import {
  ShieldHalf,
} from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { NAV_ITEMS } from '@/utils/constants';
import { cn } from '@/utils/helpers';
import { navIcons } from '@/components/layout/navIcons';

function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 shrink-0 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      <div className="flex h-20 items-center gap-3 border-b border-slate-100 px-6">
        <span className="flex h-11 w-11 items-center justify-center rounded-md bg-charcoal text-white">
          <ShieldHalf className="h-6 w-6" />
        </span>
        <div>
          <p className="text-base font-semibold text-charcoal">SecureWipe</p>
          <p className="text-xs text-slate-500">Verification Portal</p>
        </div>
      </div>

      <nav className="space-y-1 px-4 py-6">
        {NAV_ITEMS.map((item) => {
          const Icon = navIcons[item.icon];
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-mutedBlue-50 text-mutedBlue-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-charcoal',
                )
              }
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      <div className="mt-auto border-t border-slate-100 p-5">
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <p className="text-sm font-semibold text-charcoal">Compliance Mode</p>
          <p className="mt-1 text-xs leading-5 text-slate-500">
            Read-only verification workspace with retained audit evidence.
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
