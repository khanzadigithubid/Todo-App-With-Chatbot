import React from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  helperText?: string;
  containerClassName?: string;
  options: Array<{
    value: string;
    label: string;
  }>;
}

const Select: React.FC<SelectProps> = ({
  label,
  error,
  helperText,
  containerClassName = '',
  className = '',
  options,
  ...props
}) => {
  const selectClasses = `
    w-full px-4 py-3.5 rounded-xl bg-surface-light border
    ${error ? 'border-error' : 'border-border'}
    placeholder-text-muted focus:outline-none focus:ring-2
    focus:ring-primary focus:border-transparent transition-all
    duration-200 text-text-primary appearance-none
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
        <select
          className={selectClasses}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg className="h-5 w-5 text-text-secondary" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </div>
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

export default Select;