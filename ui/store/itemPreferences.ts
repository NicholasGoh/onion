// Layer 3: Zustand (global UI state)
// Client-side UI state that doesn't belong to the server

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ItemPreferencesState {
  // UI preferences
  viewMode: 'grid' | 'list';
  sortBy: 'name' | 'id';
  sortOrder: 'asc' | 'desc';

  // Actions
  setViewMode: (mode: 'grid' | 'list') => void;
  setSortBy: (field: 'name' | 'id') => void;
  toggleSortOrder: () => void;
}

export const useItemPreferences = create<ItemPreferencesState>()(
  persist(
    (set) => ({
      // Default values
      viewMode: 'list',
      sortBy: 'id',
      sortOrder: 'desc',

      // Actions
      setViewMode: (mode) => set({ viewMode: mode }),
      setSortBy: (field) => set({ sortBy: field }),
      toggleSortOrder: () =>
        set((state) => ({
          sortOrder: state.sortOrder === 'asc' ? 'desc' : 'asc',
        })),
    }),
    {
      name: 'item-preferences', // localStorage key
    }
  )
);
