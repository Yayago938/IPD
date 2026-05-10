import { NavLink } from 'react-router-dom';
import { navIcons } from '@/components/layout/navIcons';
import { NAV_ITEMS } from '@/utils/constants';
import { cn } from '@/utils/helpers';

function BottomNav() {
  return (
    <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white lg:hidden">
      <div className="grid h-16 grid-cols-4">
        {NAV_ITEMS.map((item) => {
          const Icon = navIcons[item.icon];
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex min-w-0 flex-col items-center justify-center gap-1 px-1 text-[11px] font-medium transition-colors',
                  isActive ? 'text-mutedBlue-700' : 'text-slate-500 hover:text-charcoal',
                )
              }
            >
              <Icon className="h-5 w-5" />
              <span className="truncate">{item.shortLabel || item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
}

export default BottomNav;
