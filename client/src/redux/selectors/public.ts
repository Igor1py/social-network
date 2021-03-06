import { RootState } from "../store";

export const selectPendingPosts = (state: RootState) => {
  return state.public.pendingPosts;
}

export const selectFilter = (state: RootState) => {
  return state.public.filter;
}

export const selectPosts = (state: RootState) => {
  return state.public.posts;
}

export const selectTotalPostsCount = (state: RootState) => {
  return state.public.totalPostsCount;
}

export const selectPendingLikePosts = (state: RootState) => {
  return state.public.pendingLikePosts;
}

export const selectEditingPostId = (state: RootState) => {
  return state.public.editingPostId;
}

export const selectComments = (postId: number) => (state: RootState) => {
  return state.public.comments.filter(c => c.postId === postId);
}

export const selectPendingLikeComments = (state: RootState) => {
  return state.public.pendingLikeComments;
}

export const selectEditingCommentId = (state: RootState) => {
  return state.public.editingCommentId;
}

export const selectOpenedComments = (state: RootState) => {
  return state.public.openedComments;
}

export const selectOpenedReplies = (state: RootState) => {
  return state.public.openedReplies;
}

export const selectReplies = (commentId: number) => (state: RootState) => {
  return state.public.replies.filter(r => r.commentId === commentId);
}

export const selectPendingLikeReplies = (state: RootState) => {
  return state.public.pendingLikeReplies;
}

export const selectEditingReplyId = (state: RootState) => {
  return state.public.editingReplyId;
}