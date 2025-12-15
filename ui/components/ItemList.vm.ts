// Layer 2: ViewModel for ItemList component
// Connects queries, state, and entities to prepare data for the view

import { useMemo } from 'react';
import { useItems } from '@/queries/useItems';
import { useItemPreferences } from '@/store/itemPreferences';
import { Item } from '@/lib/entities/item';

// View-specific shape for displaying an item
export interface ItemViewModel {
  id: number;
  name: string;
  description: string | null;
}

function toItemViewModel(item: Item): ItemViewModel {
  return {
    id: item.id,
    name: item.name,
    description: item.description,
  };
}

export function useItemListViewModel() {
  // Server state
  const { data: items = [], isLoading, error } = useItems();

  // UI state
  const { sortBy, sortOrder, viewMode } = useItemPreferences();

  // Derived state: sorted items
  const sortedItems = useMemo(() => {
    const sorted = [...items].sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];

      if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    return sorted.map(toItemViewModel);
  }, [items, sortBy, sortOrder]);

  return {
    items: sortedItems,
    isLoading,
    error,
    viewMode,
  };
}
