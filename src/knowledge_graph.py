import networkx as nx
from typing import Dict, List, Optional, Tuple

class KnowledgeGraph:
    """Simple directed knowledge graph wrapper around networkx.DiGraph.

    Improvements:
    - safer attribute access
    - save/load helpers
    - find_by_type/name
    - merge/update edges with aggregation of confidence
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity_id: str, entity_type: str, attributes: Optional[Dict] = None) -> None:
        if attributes is None:
            attributes = {}
        attrs_to_add = attributes.copy()
        # Avoid clobbering reserved key 'type' in attributes
        attrs_to_add.pop('type', None)
        # store declared type under 'type' node attribute
        self.graph.add_node(entity_id, type=entity_type, **attrs_to_add)

    def add_relationship(self, source_id: str, target_id: str, rel_type: str, attributes: Optional[Dict] = None) -> None:
        if attributes is None:
            attributes = {}
        if not (self.graph.has_node(source_id) and self.graph.has_node(target_id)):
            raise ValueError(f"Source {source_id} or target {target_id} not present in KG")
        # If there is already an edge with the same type, we merge confidences (take max) to avoid duplicates
        existing = self.graph.get_edge_data(source_id, target_id) or {}
        if existing and existing.get('type') == rel_type:
            # merge numeric confidences if provided
            new_conf = attributes.get('confidence')
            old_conf = existing.get('confidence')
            if new_conf is not None and old_conf is not None:
                attributes['confidence'] = max(new_conf, old_conf)
            elif new_conf is None and old_conf is not None:
                attributes['confidence'] = old_conf
        self.graph.add_edge(source_id, target_id, type=rel_type, **attributes)

    def get_neighbors(self, entity_id: str, rel_type: Optional[str] = None) -> List[str]:
        if not self.graph.has_node(entity_id):
            return []
        neighbors = []
        for neighbor in self.graph.successors(entity_id):
            edge = self.graph.get_edge_data(entity_id, neighbor) or {}
            if rel_type is None or edge.get('type') == rel_type:
                neighbors.append(neighbor)
        return neighbors

    def get_entity_attributes(self, entity_id: str) -> Optional[Dict]:
        if self.graph.has_node(entity_id):
            return dict(self.graph.nodes[entity_id])
        return None

    def query_semantic_concept(self, concept_name: str) -> List[str]:
        results = []
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get('type') == 'SemanticConcept' and attrs.get('name') == concept_name:
                for predecessor in self.graph.predecessors(node_id):
                    edge = self.graph.get_edge_data(predecessor, node_id) or {}
                    if edge.get('type') == 'INDICATES':
                        results.append(predecessor)
        return results

    # Utility helpers
    def nodes_by_type(self, node_type: str) -> List[Tuple[str, Dict]]:
        return [(n, d) for n, d in self.graph.nodes(data=True) if d.get('type') == node_type]

    def save_gpickle(self, path: str) -> None:
        nx.write_gpickle(self.graph, path)

    def load_gpickle(self, path: str) -> None:
        self.graph = nx.read_gpickle(path)


if __name__ == '__main__':
    # pequeno sanity check
    kg = KnowledgeGraph()
    kg.add_entity('s1', 'SignalSegment', {'time_start': 0, 'time_end': 250})
    kg.add_entity('c_fault', 'SemanticConcept', {'name': 'Fault'})
    kg.add_relationship('s1', 'c_fault', 'INDICATES', {'confidence': 0.8})
    print(kg.query_semantic_concept('Fault'))