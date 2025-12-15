export interface ItemCreate {
  name: string;
  description: string | null;
}

export interface ItemRead {
  id: number;
  name: string;
  description?: string | null;
}
