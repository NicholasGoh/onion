// Layer 1: Presentation (routes)
// Page component that composes other components

import { ItemList } from './ItemList';
import { useItemPreferences } from '@/store/itemPreferences';

export function ItemsPage() {
  const { viewMode, setViewMode, sortBy, setSortBy, toggleSortOrder, sortOrder } =
    useItemPreferences();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Items</h1>

      {/* Controls */}
      <div className="flex gap-4 mb-6 items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('list')}
            className={`px-3 py-1 rounded ${viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-gray-200'
              }`}
          >
            List
          </button>
          <button
            onClick={() => setViewMode('grid')}
            className={`px-3 py-1 rounded ${viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-gray-200'
              }`}
          >
            Grid
          </button>
        </div>

        <div className="flex gap-2 items-center">
          <label className="text-sm">Sort by:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
            className="px-2 py-1 border rounded"
          >
            <option value="name">Name</option>
            <option value="id">ID</option>
          </select>
          <button
            onClick={toggleSortOrder}
            className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>
      </div>

      <ItemList />
    </div>
  );
}
