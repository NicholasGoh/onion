// if variables are snakecase in api
// this file abstracts with ui DDD
// camel case

export interface Item {
  id: number;
  name: string;
  description: string | null;
}

export interface ItemData {
  name: string;
  description: string | null;
}
