import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  containerClassName?: string;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  startIcon,
  endIcon,
  containerClassName = '',
  className = '',
  ...props
}) => {
  const inputClasses = `
    w-full px-4 py-3.5 rounded-xl bg-surface-light border
    ${error ? 'border-error' : 'border-border'}
    placeholder-text-muted focus:outline-none focus:ring-2
    focus:ring-primary focus:border-primary transition-all
    duration-200 text-text-primary
    ${startIcon ? 'pl-10' : ''}
    ${endIcon ? 'pr-10' : ''}
    ${className}
  `;

  return (
    <div className={`w-full ${containerClassName}`}>
      {label && (
        <label className="block text-sm font-medium text-text-primary mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {startIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            {startIcon}
          </div>
        )}
        <input
          className={inputClasses}
          {...props}
        />
        {endIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {endIcon}
          </div>
        )}
      </div>
      {helperText && !error && (
        <p className="mt-2 text-sm text-text-secondary">{helperText}</p>
      )}
      {error && (
        <p className="mt-2 text-sm text-error">{error}</p>
      )}
    </div>
  );
};

export default Input;