"use client";

import { useEffect, useState, type FormEvent } from "react";
import {
  createPrediction,
  getMetrics,
  getSamples,
  type DemoSample,
  type ModelMetrics,
  type Prediction,
} from "@/lib/api";

const CLASS_LABELS: Record<string, string> = { benign: "Доброкачественный", malignant: "Злокачественный" };

export default function PredictionsPage() {
  const [samples, setSamples] = useState<DemoSample[]>([]);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [result, setResult] = useState<Prediction | null>(null);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [loadedSamples, loadedMetrics] = await Promise.all([getSamples(), getMetrics()]);
        setSamples(loadedSamples);
        setMetrics(loadedMetrics);
        setSelectedId(loadedSamples[0]?.id ?? null);
      } catch {
        setError("Не удалось загрузить демонстрационные образцы. Проверьте, что API запущен.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const selected = samples.find((item) => item.id === selectedId) ?? null;

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selected) return;
    setError("");
    setPending(true);
    try {
      const prediction = await createPrediction(
        selected.features,
        `Образец ${selected.id}`,
        selected.reference_class,
      );
      setResult(prediction);
    } catch {
      setError("Не удалось получить классификацию. Проверьте, что API запущен, и повторите попытку.");
    } finally {
      setPending(false);
    }
  }

  return (
    <main className="wrap page">
      <div className="eyebrow">Классификация · 01</div>
      <h1>Демонстрация WDBC-классификатора</h1>
      <p className="lead">
        Выберите готовый образец Breast Cancer Wisconsin Diagnostic и запустите учебную классификацию.
        Ручной ввод 30 признаков не требуется.
      </p>
      <div className="form-layout">
        <form className="panel" onSubmit={submit}>
          {loading && <p className="subtle">Загрузка образцов…</p>}
          {!loading && samples.length > 0 && (
            <div className="fields">
              <div className="field full">
                <label htmlFor="sample">Демонстрационный образец</label>
                <select
                  id="sample"
                  value={selectedId ?? ""}
                  onChange={(event) => setSelectedId(Number(event.target.value))}
                >
                  {samples.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.description} · эталон: {CLASS_LABELS[item.reference_class]}
                    </option>
                  ))}
                </select>
                <small>Образцы взяты из тестовой выборки WDBC и зафиксированы seed 42.</small>
              </div>
            </div>
          )}
          {selected && (
            <div className="notice" style={{ marginTop: 16 }}>
              Признаков: {Object.keys(selected.features).length} · первые 5:{" "}
              {Object.entries(selected.features)
                .slice(0, 5)
                .map(([name, value]) => `${name}=${value.toFixed(2)}`)
                .join(", ")}
            </div>
          )}
          {metrics && (
            <p className="subtle" style={{ marginTop: 12 }}>
              Holdout: accuracy {(metrics.metrics.accuracy * 100).toFixed(1)}% · ROC-AUC{" "}
              {metrics.metrics.roc_auc.toFixed(3)} · {metrics.sample_count} записей, train{" "}
              {Math.round(metrics.train_fraction * 100)}%
            </p>
          )}
          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
          <button className="button" disabled={pending || !selected} type="submit">
            {pending ? "Классификация…" : "Классифицировать образец"}
          </button>
        </form>
        <aside className="panel">
          <h2 className="aside-title">Об исследовании</h2>
          <p className="aside-copy">
            Логистическая регрессия обучается на WDBC через scikit-learn и предсказывает вероятность класса
            malignant по признакам клеточных ядер. Это учебная демонстрация диагностики, а не прогноз
            эффективности лечения.
          </p>
          {result ? (
            <div className="result" aria-live="polite">
              <span className="pill">Результат модели</span>
              <strong>{(result.malignant_probability * 100).toFixed(1)}%</strong>
              <small>
                {result.predicted_class === "malignant"
                  ? "Модель отнесла образец к злокачественному классу."
                  : "Модель отнесла образец к доброкачественному классу."}
                <br />
                Эталон образца: {CLASS_LABELS[result.reference_class] ?? result.reference_class}
                <br />
                Версия: {result.model_version}
              </small>
            </div>
          ) : (
            <div className="notice">Выберите образец и нажмите «Классифицировать образец».</div>
          )}
          <p className="aside-copy" style={{ fontSize: 11, marginTop: 18 }}>
            Не вносите персональные данные. Результат не является диагнозом.
          </p>
        </aside>
      </div>
    </main>
  );
}
