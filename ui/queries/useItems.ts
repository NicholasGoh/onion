// Layer 3: TanStack Query (server state orchestration)
// Handles caching, refetching, and server state synchronization

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { itemRepository } from '@/lib/business/itemRepository';
import { ItemData } from '@/lib/entities/item';

// Query keys for cache management
export const itemKeys = {
  all: ['items'] as const,
  lists: () => [...itemKeys.all, 'list'] as const,
  list: (filters?: unknown) => [...itemKeys.lists(), filters] as const,
  details: () => [...itemKeys.all, 'detail'] as const,
  detail: (id: number) => [...itemKeys.details(), id] as const,
};

// Fetch single item
export function useItem(id: number) {
  return useQuery({
    queryKey: itemKeys.detail(id),
    queryFn: () => itemRepository.getItem(id),
  });
}

// Fetch all items
export function useItems() {
  return useQuery({
    queryKey: itemKeys.lists(),
    queryFn: () => itemRepository.getItems(),
  });
}

// Create item mutation
export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: ItemData) => itemRepository.createItem(input),
    onSuccess: () => {
      // Invalidate and refetch items list
      queryClient.invalidateQueries({ queryKey: itemKeys.lists() });
    },
  });
}
