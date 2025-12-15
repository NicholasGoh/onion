// Layer 2: ItemList component
// Pure presentation component using ViewModel

import { useItemListViewModel, ItemViewModel } from './ItemList.vm';

interface ItemDisplayProps {
  item: ItemViewModel;
}

function ItemDisplay({ item }: ItemDisplayProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <h3 className="font-semibold text-lg">{item.name}</h3>
        <span className="text-xs text-gray-400">#{item.id}</span>
      </div>
      {item.description && (
        <p className="text-gray-600 mt-2 text-sm">{item.description}</p>
      )}
    </div>
  );
}

export function ItemList() {
  const { items, isLoading, error, viewMode } = useItemListViewModel();

  if (isLoading) {
    return <div className="text-center py-8">Loading items...</div>;
  }

  if (error) {
    return (
      <div className="text-red-600 py-8">
        Error loading items: {error instanceof Error ? error.message : 'Unknown error'}
      </div>
    );
  }

  if (items.length === 0) {
    return <div className="text-gray-500 py-8">No items found</div>;
  }

  return (
    <div
      className={
        viewMode === 'grid'
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
          : 'space-y-4'
      }
    >
      {items.map((item) => (
        <ItemDisplay key={item.id} item={item} />
      ))}
    </div>
  );
}
