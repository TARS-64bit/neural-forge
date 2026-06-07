import "./globals.css";
import Providers from "./providers";

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark">
      <body
        style={{ backgroundImage: "url('/bg.jpg')", backgroundSize: "cover", backgroundPosition: "center" }}
        className="bg-zinc-950 text-zinc-50 min-h-screen antialiased selection:bg-cyan-500/30 ">

        <Providers>{children}</Providers>
      </body>
    </html>
  );
}