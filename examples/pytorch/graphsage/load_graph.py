import torch as th

import dgl


def load_reddit(self_loop=True):
    from dgl.data import RedditDataset

    # load reddit data
    data = RedditDataset(self_loop=self_loop)
    g = data[0]
    g.ndata["features"] = g.ndata.pop("feat")
    g.ndata["labels"] = g.ndata.pop("label")
    return g, data.num_classes

def load_mag240m(root="dataset"):
    from ogb.lsc import MAG240MDataset
    import numpy as np
    from os.path import join

    dataset = MAG240MDataset(root=root)

    print("Loading graph")
    (g,), _ = dgl.load_graphs(join(root, 'mag240m_kddcup2021/graph.dgl'))

    print("Loading features")
    paper_offset = dataset.num_authors + dataset.num_institutions
    num_nodes = paper_offset + dataset.num_papers
    num_features = dataset.num_paper_features
    feats = th.from_numpy(np.memmap(
        join(root, 'mag240m_kddcup2021/full.npy'),
        mode="r",
        dtype="float16",
        shape=(num_nodes, num_features),
        ))
    g.ndata["features"] = feats
    train_nid = th.tensor(dataset.get_idx_split("train"), dtype=th.int64) + paper_offset
    val_nid = th.tensor(dataset.get_idx_split("valid"), dtype=th.int64) + paper_offset
    test_nid = th.tensor(dataset.get_idx_split("test-dev"), dtype=th.int64) + paper_offset
    train_mask = th.zeros((g.number_of_nodes(),), dtype=th.bool)
    train_mask[train_nid] = True
    val_mask = th.zeros((g.number_of_nodes(),), dtype=th.bool)
    val_mask[val_nid] = True
    test_mask = th.zeros((g.number_of_nodes(),), dtype=th.bool)
    test_mask[test_nid] = True
    g.ndata["train_mask"] = train_mask
    g.ndata["val_mask"] = val_mask
    g.ndata["test_mask"] = test_mask
    labels = th.tensor(dataset.paper_label, dtype=th.uint8)
    num_labels = len(th.unique(labels[th.logical_not(th.isnan(labels))]))
    g.ndata["labels"] = - th.ones(g.number_of_nodes(), dtype=th.uint8)
    g.ndata["labels"][train_nid] = labels[train_nid - paper_offset]
    g.ndata["labels"][val_nid] = labels[val_nid - paper_offset]
    g.edata['etype'] = g.edata['etype'].to(th.int8)
    return g, num_labels

def load_ogb(name, root="dataset"):
    if name == "ogbn-mag240M":
        return load_mag240m(root)

    from ogb.nodeproppred import DglNodePropPredDataset

    print("load", name)
    data = DglNodePropPredDataset(name=name, root=root)
    print("finish loading", name)
    splitted_idx = data.get_idx_split()
    graph, labels = data[0]
    labels = labels[:, 0]

    graph.ndata["features"] = graph.ndata.pop("feat")
    graph.ndata["labels"] = labels.long()
    in_feats = graph.ndata["features"].shape[1]
    num_labels = len(th.unique(labels[th.logical_not(th.isnan(labels))]))

    # Find the node IDs in the training, validation, and test set.
    train_nid, val_nid, test_nid = (
        splitted_idx["train"],
        splitted_idx["valid"],
        splitted_idx["test"],
    )
    train_mask = th.zeros((graph.number_of_nodes(),), dtype=th.bool)
    train_mask[train_nid] = True
    val_mask = th.zeros((graph.number_of_nodes(),), dtype=th.bool)
    val_mask[val_nid] = True
    test_mask = th.zeros((graph.number_of_nodes(),), dtype=th.bool)
    test_mask[test_nid] = True
    graph.ndata["train_mask"] = train_mask
    graph.ndata["val_mask"] = val_mask
    graph.ndata["test_mask"] = test_mask
    print("finish constructing", name)
    return graph, num_labels

def inductive_split(g):
    """Split the graph into training graph, validation graph, and test graph by training
    and validation masks.  Suitable for inductive models."""
    train_g = g.subgraph(g.ndata["train_mask"])
    val_g = g.subgraph(g.ndata["train_mask"] | g.ndata["val_mask"])
    test_g = g
    return train_g, val_g, test_g
