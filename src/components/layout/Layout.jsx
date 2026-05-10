import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-charcoal">
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <Header />
          <main className="flex-1 px-5 py-8 sm:px-8">{children}</main>
        </div>
      </div>
    </div>
  );
}

export default Layout;
