import { getHistory } from "@/lib/api";

const classLabels: Record<string, string> = {
  benign: "Доброкачественный",
  malignant: "Злокачественный",
  неизвестно: "Неизвестно",
  unknown: "Неизвестно",
};

export default async function HistoryPage() {
  try {
    const entries = await getHistory();
    return (
      <main className="wrap page">
        <div className="eyebrow">Эксперименты · 02</div>
        <h1>История классификаций</h1>
        <p className="lead">Сохранённые учебные классификации WDBC-образцов.</p>
        {entries.length === 0 ? (
          <div className="panel" style={{ marginTop: 28 }}>
            <p className="subtle">
              Пока нет расчётов. Запустите первую классификацию на странице{" "}
              <a href="/predictions">
                <u>нового прогноза</u>
              </a>
              .
            </p>
          </div>
        ) : (
          <div className="table-wrap" style={{ marginTop: 28 }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Дата</th>
                  <th>Образец</th>
                  <th>Эталон</th>
                  <th>Класс модели</th>
                  <th>P(malignant)</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((item) => (
                  <tr key={item.id}>
                    <td>{new Date(item.created_at).toLocaleString("ru-RU")}</td>
                    <td>{item.sample_name}</td>
                    <td>{classLabels[item.reference_class] ?? item.reference_class}</td>
                    <td>{classLabels[item.predicted_class] ?? item.predicted_class}</td>
                    <td>
                      <span className="pill">{(item.malignant_probability * 100).toFixed(1)}%</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <div className="notice" style={{ marginTop: 20 }}>
          Учебные метки WDBC; результат не является диагнозом и не оценивает эффективность лечения.
        </div>
      </main>
    );
  } catch {
    return (
      <main className="wrap page">
        <div className="eyebrow">Эксперименты · 02</div>
        <h1>История классификаций</h1>
        <p className="error">Не удалось подключиться к API. Проверьте, что backend запущен.</p>
      </main>
    );
  }
}
