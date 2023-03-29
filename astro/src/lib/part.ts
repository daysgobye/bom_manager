export type RawPart = {
  name?: string;
  package: string;
  value: string;
  part_number: string;
  qty?: number;
  note?: string;
  location?: string;
  dataSheet?: string;
};

export interface FullPart extends RawPart {
  id: number;
  owner?: any;
  userId?: number;
  missing: boolean;
  rollback: boolean;
  incoming: boolean;
  lookup: boolean;
}
