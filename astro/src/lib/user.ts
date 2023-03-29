import { FullPart } from "./part";

export default class User {
  id: number;
  token: string;
  partLibrary: FullPart[];
  constructor(userData) {
    this.id = userData.id;
    this.token = userData.token;
    this.partLibrary = userData.partLibrary;
  }

  findPartInLibrary = (pkg: string, value: string, part_number: string) => {
    return this.partLibrary.find(
      (part) =>
        part.part_number === part_number ||
        (part.value === value && part.package === pkg)
    );
  };
}
