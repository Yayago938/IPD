import { X, ShieldHalf } from 'lucide-react';
import { useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import Button from '@/components/ui/Button';
import { navIcons } from '@/components/layout/navIcons';
import { NAV_ITEMS } from '@/utils/constants';
import { cn } from '@/utils/helpers';

function MobileDrawer({ open, onClose }) {
  const location = useLocation();

  useEffect(() => {
    onClose();
  }, [location.pathname, onClose]);

  useEffect(() => {
    if (!open) return undefined;

    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.body.style.overflow = originalOverflow;
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [open, onClose]);

  return (
    <div
      className={cn(
        'fixed inset-0 z-50 lg:hidden',
        open ? 'pointer-events-auto' : 'pointer-events-none',
      )}
      aria-hidden={!open}
    >
      <button
        type="button"
        className={cn(
          'absolute inset-0 bg-slate-950/40 transition-opacity duration-200',
          open ? 'opacity-100' : 'opacity-0',
        )}
        aria-label="Close navigation"
        onClick={onClose}
      />
      <aside
        className={cn(
          'absolute inset-y-0 left-0 flex w-[min(19rem,85vw)] flex-col border-r border-slate-200 bg-white shadow-panel transition-transform duration-300 ease-out',
          open ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-20 items-center justify-between gap-3 border-b border-slate-100 px-5">
          <div className="flex min-w-0 items-center gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-charcoal text-white">
              <ShieldHalf className="h-5 w-5" />
            </span>
            <div className="min-w-0">
              <p className="truncate text-base font-semibold text-charcoal">SecureWipe</p>
              <p className="truncate text-xs text-slate-500">Verification Portal</p>
            </div>
          </div>
          <Button aria-label="Close navigation" size="icon" variant="ghost" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        <nav className="space-y-1 px-4 py-5">
          {NAV_ITEMS.map((item) => {
            const Icon = navIcons[item.icon];
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 rounded-md px-3 py-3 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-mutedBlue-50 text-mutedBlue-700'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-charcoal',
                  )
                }
              >
                <Icon className="h-5 w-5" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-auto border-t border-slate-100 p-5">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Mobile audit workspace
          </p>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Navigate verification evidence, reports, and settings without leaving the secure review
            context.
          </p>
        </div>
      </aside>
    </div>
  );
}

export default MobileDrawer;
