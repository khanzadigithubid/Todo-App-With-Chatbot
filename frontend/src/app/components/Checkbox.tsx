import React from 'react';

interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  containerClassName?: string;
}

const Checkbox: React.FC<CheckboxProps> = ({
  label,
  error,
  containerClassName = '',
  ...props
}) => {
  return (
    <div className={`flex items-start ${containerClassName}`}>
      <div className="flex items-center h-5">
        <input
          type="checkbox"
          className={`h-4 w-4 text-primary focus:ring-primary border-border rounded bg-surface-light ${
            error ? 'border-error' : ''
          }`}
          {...props}
        />
      </div>
      <div className="ml-3 text-sm">
        {label && (
          <label className="font-medium text-text-primary">
            {label}
          </label>
        )}
        {error && (
          <p className="text-error">{error}</p>
        )}
      </div>
    </div>
  );
};

export default Checkbox;