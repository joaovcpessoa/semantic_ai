import numpy as np
from dl_model import DLModel
from typing import List, Tuple, Optional
from knowledge_graph import KnowledgeGraph
from signal_processor import SignalProcessor

class SemanticAnalyzer:
    def __init__(self, sampling_rate: int, segment_length: int, dl_input_shape: Tuple[int, ...], num_classes: int = 2, threshold: float = 0.3):
        self.signal_processor = SignalProcessor(sampling_rate)
        self.dl_model = DLModel(dl_input_shape, num_classes)
        self.kg = KnowledgeGraph()
        self.segment_length = segment_length
        self.threshold = threshold

        # conceitos base
        self.kg.add_entity('concept_significant_bit', 'SemanticConcept', {'name': 'SignificantBit'})
        self.kg.add_entity('concept_non_significant_bit', 'SemanticConcept', {'name': 'NonSignificantBit'})

    def analyze_signal(self, raw_signal: np.ndarray, train_dl: bool = False, X_train_dl: Optional[np.ndarray] = None, y_train_dl: Optional[np.ndarray] = None) -> Tuple[List[Tuple[str, str, float]], KnowledgeGraph]:
        processed = self.signal_processor.preprocess_signal(raw_signal)
        segments = self.signal_processor.segment_signal(processed, self.segment_length)
        X_segments = np.array(segments)

        if X_segments.size == 0:
            return [], self.kg

        if train_dl and X_train_dl is not None and y_train_dl is not None:
            self.dl_model.train(X_train_dl, y_train_dl)

        # modelo pode retornar probabilidades (shape=(N,)) ou logits/classes
        raw_preds = self.dl_model.predict_significance(X_segments)
        # normalize to probabilities in [0,1]
        preds = self._ensure_probabilities(raw_preds)

        results = []
        for i, prob in enumerate(preds):
            seg_id = f'segment_{i:03d}'
            self.kg.add_entity(seg_id, 'SignalSegment', {'index': i, 'data_preview': segments[i][:8].tolist()})

            if prob >= self.threshold:
                self.kg.add_relationship(seg_id, 'concept_significant_bit', 'INDICATES', {'confidence': float(prob)})
                results.append((seg_id, 'SignificantBit', float(prob)))
            else:
                conf = 1.0 - float(prob)
                self.kg.add_relationship(seg_id, 'concept_non_significant_bit', 'INDICATES', {'confidence': conf})
                results.append((seg_id, 'NonSignificantBit', conf))

        return results, self.kg

    def _ensure_probabilities(self, raw_preds: np.ndarray) -> np.ndarray:
        arr = np.array(raw_preds)
        # if multi-d output like (N,2), take probability of class 1
        if arr.ndim == 2 and arr.shape[1] == 2:
            probs = arr[:, 1]
        elif arr.ndim == 1:
            # if already in [0,1] accept, otherwise apply sigmoid
            if np.all((arr >= 0) & (arr <= 1)):
                probs = arr
            else:
                probs = 1 / (1 + np.exp(-arr))
        else:
            # fallback: flatten and sigmoid
            probs = 1 / (1 + np.exp(-arr.flatten()))
        return probs

    def add_context_to_kg(self, segment_id: str, context_entity_id: str, context_type: str, attributes: Optional[dict] = None) -> None:
        attrs = attributes.copy() if attributes else {}
        if 'type' in attrs:
            # avoid shadowing
            attrs[f'{context_type.lower()}_type'] = attrs.pop('type')
        self.kg.add_entity(context_entity_id, context_type, attrs)
        self.kg.add_relationship(segment_id, context_entity_id, 'HAS_CONTEXT')

    # stub for XAI per-segment explanation (to be implemented using XAIExplainer)
    def explain_segment(self, segment_index: int, explainer) -> dict:
        # explainer expected to have method explain(X, idx) or similar
        raise NotImplementedError('Use your XAIExplainer to implement explanations per segment')


if __name__ == '__main__':
    print('Run semantic_analyzer unit tests separately')