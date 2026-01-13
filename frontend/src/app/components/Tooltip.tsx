import { ReactNode } from 'react';

interface TooltipProps {
  children: ReactNode;
  content: ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

export default function Tooltip({ children, content, position = 'top' }: TooltipProps) {
  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  };

  return (
    <div className="relative inline-block">
      <div className="group">
        {children}
        <div className={`absolute z-50 hidden group-hover:block ${positionClasses[position]} w-max max-w-xs px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm`}>
          {content}
          <div className={`absolute w-2 h-2 bg-gray-900 rotate-45 ${position === 'top' ? 'bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2' : 
            position === 'bottom' ? 'top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2' : 
            position === 'left' ? 'right-0 top-1/2 transform translate-x-1/2 -translate-y-1/2' : 
            'left-0 top-1/2 transform -translate-x-1/2 -translate-y-1/2'}`}></div>
        </div>
      </div>
    </div>
  );
}