import { cn } from '@/utils/helpers';

function Input({ label, hint, className = '', id, ...props }) {
  const inputId = id || props.name;

  return (
    <label className="block" htmlFor={inputId}>
      {label ? <span className="mb-2 block text-sm font-medium text-slate-700">{label}</span> : null}
      <input
        id={inputId}
        className={cn(
          'focus-ring h-11 w-full rounded-md border border-slate-200 bg-white px-3 text-sm text-charcoal placeholder:text-slate-400',
          className,
        )}
        {...props}
      />
      {hint ? <span className="mt-2 block text-xs text-slate-500">{hint}</span> : null}
    </label>
  );
}

export default Input;
