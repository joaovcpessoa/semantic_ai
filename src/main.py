import numpy as np
from knowledge_graph import KnowledgeGraph
from semantic_analyzer import SemanticAnalyzer

# os módulos abaixo precisam existir; veja stubs sugeridos mais abaixo
from synthetic_data_generator import SyntheticDataGenerator
from signal_processor import SignalProcessor
from dl_model import DLModel
from precoder_optimizer import PreCoderOptimizer
from xai_explainer import XAIExplainer
from visualizer import Visualizer

if __name__ == '__main__':
    sampling_rate = 1000
    duration = 120
    segment_length = 250

    data_generator = SyntheticDataGenerator(sampling_rate=sampling_rate, duration=duration)
    signal_processor = SignalProcessor(sampling_rate=sampling_rate)
    dl_model_instance = DLModel(input_shape=(segment_length, 1), num_classes=2)
    kg_instance = KnowledgeGraph()
    semantic_analyzer = SemanticAnalyzer(
        sampling_rate=sampling_rate,
        segment_length=segment_length,
        dl_input_shape=(segment_length, 1)
    )
    precoder_optimizer = PreCoderOptimizer()
    xai_explainer = XAIExplainer(dl_model_instance)
    visualizer = Visualizer(sampling_rate, segment_length)

    print('\n--- Gerando dados sintéticos ---')
    raw_signal = data_generator.generate_base_signal()
    all_labels = np.zeros(len(data_generator.time_vector), dtype=int)

    # exemplos de injeção (mantenha como você já tinha)
    raw_signal, labels1 = data_generator.inject_significant_bit(raw_signal, 5, 6, bit_type='pulse', params={'amplitude': 3.0, 'frequency': 120.0})
    all_labels = np.logical_or(all_labels, labels1).astype(int)
    context1 = data_generator.generate_context(5, 6, 'sensor_A', 'EngineRoom', 'HighTemp')

    # ... outros cenários ...

    processed_signal_for_dl = signal_processor.preprocess_signal(raw_signal)
    segments_for_dl = signal_processor.segment_signal(processed_signal_for_dl, segment_length)

    X_train_dl = np.array(segments_for_dl)

    # Mapear rótulos de amostra para segmento (com bordas preservadas)
    y_train_dl = np.zeros(len(segments_for_dl), dtype=int)
    for i in range(len(segments_for_dl)):
        start_sample_of_segment = i * segment_length
        end_sample_of_segment = min(start_sample_of_segment + segment_length, len(all_labels))
        if start_sample_of_segment >= len(all_labels):
            break
        significant_samples_in_segment = np.sum(all_labels[start_sample_of_segment:end_sample_of_segment] == 1)
        if significant_samples_in_segment > (segment_length * 0.01):
            y_train_dl[i] = 1

    print(f'Shape X: {X_train_dl.shape}, Shape y: {y_train_dl.shape}, Significant segments: {np.sum(y_train_dl)}')

    print('\n--- Análise Semântica e treinar DL ---')
    analysis_results, updated_kg = semantic_analyzer.analyze_signal(raw_signal, train_dl=True, X_train_dl=X_train_dl, y_train_dl=y_train_dl)

    print('\n--- Resultados (exemplo) ---')
    for seg_id, concept, conf in analysis_results[:10]:
        print(seg_id, concept, conf)

    # adição de contexto (como no seu fluxo)
    def add_context_to_segments(context_info):
        start_idx_context = int(context_info['start_time'] * sampling_rate)
        end_idx_context = int(context_info['end_time'] * sampling_rate)
        for i in range(len(segments_for_dl)):
            segment_start_sample = i * segment_length
            segment_end_sample = segment_start_sample + segment_length
            if max(start_idx_context, segment_start_sample) < min(end_idx_context, segment_end_sample):
                segment_id = f'segment_{i:03d}'
                semantic_analyzer.add_context_to_kg(
                    segment_id,
                    f"device_{context_info['device_id']}",
                    'Device',
                    {'location': context_info['location'], 'id': context_info['device_id'], 'device_type': 'VibrationSensor'}
                )
                semantic_analyzer.add_context_to_kg(
                    segment_id,
                    f"env_{context_info['environmental_condition']}",
                    'EnvironmentalCondition',
                    {'value': context_info['environmental_condition'], 'condition_type': 'Environmental'}
                )

    add_context_to_segments(context1)

    print('Contextos adicionados ao KG.')

    # otimização/visualização/explainability seguem igual