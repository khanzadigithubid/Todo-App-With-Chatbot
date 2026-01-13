import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  border?: boolean;
  shadow?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  header,
  footer,
  border = true,
  shadow = true,
  padding = 'md',
}) => {
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const cardClasses = `
    bg-surface rounded-2xl
    ${border ? 'border border-border' : ''}
    ${shadow ? 'shadow-lg' : ''}
    ${className}
  `;

  return (
    <div className={cardClasses}>
      {header && (
        <div className={`border-b border-border ${paddingClasses[padding]}`}>
          {header}
        </div>
      )}
      <div className={!header ? paddingClasses[padding] : ''}>
        {children}
      </div>
      {footer && (
        <div className={`border-t border-border ${paddingClasses[padding]}`}>
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;