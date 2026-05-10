import { Bell, Menu, Search } from 'lucide-react';
import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import Button from '@/components/ui/Button';
import { APP_NAME, NAV_ITEMS } from '@/utils/constants';

function Header({ onMenuClick }) {
  const location = useLocation();
  const pageTitle = useMemo(() => {
    return NAV_ITEMS.find((item) => item.path === location.pathname)?.label || 'Dashboard';
  }, [location.pathname]);

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="flex h-16 items-center justify-between gap-3 px-4 sm:px-6 lg:h-20 lg:px-8">
        <div className="flex min-w-0 items-center gap-3">
          <Button
            className="shrink-0 lg:hidden"
            size="icon"
            variant="ghost"
            aria-label="Open navigation"
            onClick={onMenuClick}
          >
            <Menu className="h-5 w-5" />
          </Button>
          <div className="min-w-0">
            <p className="hidden truncate text-sm text-slate-500 sm:block">{APP_NAME}</p>
            <h1 className="truncate text-lg font-semibold text-charcoal sm:text-xl">
              {pageTitle === 'Dashboard' ? 'Verification Operations' : pageTitle}
            </h1>
          </div>
        </div>

        <div className="hidden w-full max-w-sm items-center gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-500 md:flex">
          <Search className="h-4 w-4" />
          <span>Search certificates, jobs, or audit IDs</span>
        </div>

        <div className="flex shrink-0 items-center gap-2 sm:gap-3">
          <Button size="icon" variant="secondary" aria-label="Notifications">
            <Bell className="h-4 w-4" />
          </Button>
          <div className="hidden items-center gap-3 sm:flex">
            <span className="flex h-10 w-10 items-center justify-center rounded-md bg-slate-200 text-sm font-semibold text-charcoal">
              SC
            </span>
            <div>
              <p className="text-sm font-medium text-charcoal">Security Console</p>
              <p className="text-xs text-slate-500">Audit workspace</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
