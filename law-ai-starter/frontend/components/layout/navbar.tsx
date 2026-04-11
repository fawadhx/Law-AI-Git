import Link from "next/link";

export function Navbar() {
  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <Link href="/" className="brand">
          Law AI
        </Link>

        <nav className="nav-links">
          <Link href="/">Home</Link>
          <Link href="/chat">Chat</Link>
          <Link href="/admin">Admin</Link>
        </nav>
      </div>
    </header>
  );
}
