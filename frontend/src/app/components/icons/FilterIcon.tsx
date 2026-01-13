import { Filter } from 'lucide-react';

export default function FilterIcon({ className }: { className?: string }) {
  return <Filter className={className || "h-5 w-5 text-gray-500"} />;
}
