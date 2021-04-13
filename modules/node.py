"""The module for the Node class.

Classes:
    Node

"""
from __future__ import annotations

from typing import Optional, Union

from rdflib import BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDFS

from modules.nampi_graph import Nampi_graph


class Node:
    """A node in the RDF graph."""

    _graph: Nampi_graph
    node: Union[URIRef, BNode]

    def __init__(
        self,
        graph: Nampi_graph,
        type_uri: URIRef,
        ns: Optional[Namespace] = None,
        label: Optional[str] = None,
        distinct: Optional[bool] = False
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the node belongs to.
            type_uri: The URI of the nodes' type.
            ns: An optional namespace the nodes' URI will belong to.
            label: An optional label for the node.
            distinct: An optional bool that signifies whether or not to consider the node as a distinct node that shouldn't be reused based on its label
        """
        self._graph = graph
        if label and ns and not distinct:
            self.node = self._graph.add_labeled_resource(ns, type_uri, label)
        elif ns:
            self.node = self._graph.add_resource(ns, type_uri)
            if label:
                self.add_relationship(
                    obj=Literal(label), pred=RDFS.label)
        else:
            self.node = self._graph.add_blind(type_uri)

    def add_relationship(
        self, pred: URIRef, obj: Union[Node, URIRef, BNode, Literal]
    ) -> None:
        """Add an relationship triple with the node as subject to the graph.

        Parameters:
            pred: The predicate for the resulting relationship.
            obj: The object node.
        """
        self._graph.add(
            self.node,
            pred,
            getattr(obj, "node", obj),
        )
