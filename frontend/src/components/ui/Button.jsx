import { cn } from '@/utils/helpers';

const variants = {
  primary: 'bg-mutedBlue-600 text-white border-mutedBlue-600 hover:bg-mutedBlue-700',
  secondary: 'bg-white text-charcoal border-slate-200 hover:bg-slate-50',
  ghost: 'bg-transparent text-slate-600 border-transparent hover:bg-slate-100',
  danger: 'bg-white text-red-700 border-red-200 hover:bg-red-50',
};

function Button({
  children,
  className = '',
  variant = 'primary',
  size = 'md',
  type = 'button',
  as: Component = 'button',
  ...props
}) {
  const sizes = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 text-sm',
    lg: 'h-11 px-5 text-base',
    icon: 'h-10 w-10 p-0',
  };

  return (
    <Component
      type={Component === 'button' ? type : undefined}
      className={cn(
        'focus-ring inline-flex items-center justify-center gap-2 rounded-md border font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-60',
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    >
      {children}
    </Component>
  );
}

export default Button;
