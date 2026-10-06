import Link from "next/link";

export default function HomePage() {
  return (
    <main className="wrap">
      <section className="hero">
        <div>
          <div className="eyebrow">Платформа исследовательского прототипа</div>
          <h1>Классификация WDBC машинным обучением</h1>
          <p className="lead">
            Учебная демонстрация: логистическая регрессия различает доброкачественные и злокачественные
            образцы Breast Cancer Wisconsin Diagnostic. Это не прогноз эффективности лечения и не диагноз.
          </p>
          <Link className="button" href="/predictions">
            Перейти к классификации <span aria-hidden="true">&nbsp;→</span>
          </Link>
        </div>
        <div className="model-card">
          <div className="model-label">WDBC-классификатор · учебный пример</div>
          <div className="big-number">
            ML <span style={{ color: "#54836a" }}>/</span> 01
          </div>
          <div className="subtle">Логистическая регрессия · 569 записей · 30 признаков</div>
          <div className="mini-bars" aria-hidden="true">
            <b style={{ height: "22px" }} />
            <b style={{ height: "36px" }} />
            <b style={{ height: "27px" }} />
            <b style={{ height: "45px" }} />
            <b style={{ height: "33px" }} />
            <b style={{ height: "49px" }} />
            <b style={{ height: "39px" }} />
          </div>
          <div className="subtle">Вероятность malignant — учебная оценка, не клинический показатель</div>
        </div>
      </section>
      <section style={{ paddingBottom: 12 }}>
        <h2 className="section-title">Исследовательский цикл</h2>
      </section>
      <section className="features">
        <article className="feature">
          <span className="number">01 / ДАННЫЕ</span>
          <h3>Выберите образец</h3>
          <p>Готовые примеры WDBC подставляются автоматически, вводить 30 признаков вручную не нужно.</p>
        </article>
        <article className="feature">
          <span className="number">02 / МОДЕЛЬ</span>
          <h3>Получите класс</h3>
          <p>Pipeline StandardScaler + LogisticRegression возвращает вероятность злокачественного класса.</p>
        </article>
        <article className="feature">
          <span className="number">03 / ИСТОРИЯ</span>
          <h3>Сравните результаты</h3>
          <p>Классификации с эталонной меткой сохраняются и доступны в истории экспериментов.</p>
        </article>
      </section>
    </main>
  );
}
