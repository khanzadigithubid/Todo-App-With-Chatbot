import { Search } from 'lucide-react';

export default function SearchIcon({ className }: { className?: string }) {
  return <Search className={className || "h-5 w-5 text-gray-500"} />;
}
