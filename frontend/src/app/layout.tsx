import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "ОнкоОтвет — исследовательская система",
  description: "Учебный демонстрационный прогноз на синтетических данных.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ru">
      <body>
        <header className="topbar">
          <nav className="nav wrap">
            <Link className="brand" href="/">Онко<span>Ответ</span></Link>
            <div className="navlinks"><Link href="/predictions">Новый прогноз</Link><Link href="/history">История</Link></div>
            <span className="status"><i /> Исследовательская демо-версия</span>
          </nav>
        </header>
        {children}
        <footer className="footer wrap">Прототип для исследовательских целей. Не предназначен для медицинских решений.</footer>
      </body>
    </html>
  );
}
