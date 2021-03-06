export type User = {
  id: number,
  login: string,
  photoUrl: string
}

export type Contacts = {
  github: string,
  telegram: string,
  email: string,
  vk: string,
  facebook: string,
  twitter: string,
  instagram: string,
  phoneNumber: string
}

export type Profile = {
  userId: number,
  login: string,
  photoUrl: string,
  firstName: string,
  lastName: string,
  contacts: Contacts,
  about: string,
  followersCount: number
}

export type Category = "programming" | "travels" | "countries"
  | "languages" | "politics" | "news" | "blog" | "stories"
  | "music" | "education" | "science" | "films" | "cinema"
  | "theater" | "tourism" | "statistics" | "philosophy"
  | "literature" | "psychology" | "other" | "no category";

export type Post = {
  id: number,
  category: Category,
  content: string,
  author: User,
  created: Date,
  commentsCount: number,
  likesCount: number,
  isLiked: boolean
}

export type Comment = {
  id: number,
  postId: number,
  content: string,
  author: User,
  created: Date,
  repliesCount: number,
  likesCount: number,
  isLiked: boolean
}

export type Reply = {
  id: number,
  commentId: number,
  content: string,
  author: User,
  created: Date,
  likesCount: number,
  isLiked: boolean
}