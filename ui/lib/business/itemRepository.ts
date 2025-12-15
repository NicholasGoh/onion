import { ItemRead, ItemCreate } from '../api/contracts/item';
import { Item, ItemData } from '../entities/item';

// Mappers: API → Entity
// In this case, API and Entity have the same shape, so minimal transformation
function toItem(dto: ItemRead): Item {
  return {
    id: dto.id,
    name: dto.name,
    description: dto.description ?? null,
  };
}

// Mappers: Entity → API
function toCreateItemDTO(input: ItemData): ItemCreate {
  return {
    name: input.name,
    description: input.description,
  };
}

// API Client abstraction
const api = {
  get: async <T>(url: string): Promise<T> => {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();
  },
  post: async <T>(url: string, body: unknown): Promise<T> => {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();
  },
};

// Handles API ↔ Entity mapping
export const itemRepository = {
  async getItem(id: number): Promise<Item> {
    const dto = await api.get<ItemRead>(`/api/items/${id}`);
    return toItem(dto);
  },

  async getItems(): Promise<Item[]> {
    const dtos = await api.get<ItemRead[]>('/api/items');
    return dtos.map(toItem);
  },

  async createItem(input: ItemData): Promise<Item> {
    const dto = toCreateItemDTO(input);
    const response = await api.post<ItemRead>('/api/items', dto);
    return toItem(response);
  },
};
