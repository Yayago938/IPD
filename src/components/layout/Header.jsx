import { Bell, Menu, Search } from 'lucide-react';
import Button from '@/components/ui/Button';
import { APP_NAME } from '@/utils/constants';

function Header() {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="flex h-20 items-center justify-between gap-4 px-5 sm:px-8">
        <div className="flex min-w-0 items-center gap-3">
          <Button className="lg:hidden" size="icon" variant="ghost" aria-label="Open navigation">
            <Menu className="h-5 w-5" />
          </Button>
          <div className="min-w-0">
            <p className="truncate text-sm text-slate-500">{APP_NAME}</p>
            <h1 className="truncate text-xl font-semibold text-charcoal">
              Verification Operations
            </h1>
          </div>
        </div>

        <div className="hidden w-full max-w-sm items-center gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-500 md:flex">
          <Search className="h-4 w-4" />
          <span>Search certificates, jobs, or audit IDs</span>
        </div>

        <div className="flex items-center gap-3">
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
