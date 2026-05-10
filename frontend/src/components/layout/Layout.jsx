import { useCallback, useState } from 'react';
import BottomNav from '@/components/layout/BottomNav';
import Header from '@/components/layout/Header';
import MobileDrawer from '@/components/layout/MobileDrawer';
import Sidebar from '@/components/layout/Sidebar';

function Layout({ children }) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const openDrawer = useCallback(() => setDrawerOpen(true), []);
  const closeDrawer = useCallback(() => setDrawerOpen(false), []);

  return (
    <div className="min-h-screen overflow-x-hidden bg-slate-50 text-charcoal">
      <div className="min-h-screen lg:pl-72">
        <Sidebar />
        <MobileDrawer open={drawerOpen} onClose={closeDrawer} />
        <div className="flex min-w-0 flex-1 flex-col">
          <Header onMenuClick={openDrawer} />
          <main className="flex-1 px-4 pb-24 pt-6 sm:px-6 sm:py-8 lg:px-8 lg:pb-8">
            {children}
          </main>
          <BottomNav />
        </div>
      </div>
    </div>
  );
}

export default Layout;
