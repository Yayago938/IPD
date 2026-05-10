import { cn } from '@/utils/helpers';

function Card({ children, className = '' }) {
  return (
    <section className={cn('rounded-lg border border-slate-200 bg-white shadow-panel', className)}>
      {children}
    </section>
  );
}

function CardHeader({ children, className = '' }) {
  return <div className={cn('border-b border-slate-100 px-6 py-5', className)}>{children}</div>;
}

function CardTitle({ children, className = '' }) {
  return <h2 className={cn('text-base font-semibold text-charcoal', className)}>{children}</h2>;
}

function CardContent({ children, className = '' }) {
  return <div className={cn('px-6 py-5', className)}>{children}</div>;
}

Card.Header = CardHeader;
Card.Title = CardTitle;
Card.Content = CardContent;

export default Card;
