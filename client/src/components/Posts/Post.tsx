import React from "react";
import { NavLink } from "react-router-dom";
import { FormattedDate, FormattedMessage } from "react-intl";
import { List, Avatar, Button } from "antd";
import { MessageOutlined, LikeOutlined, LikeFilled } from '@ant-design/icons';
import { Post } from "../../types/models";
import IconCount from "../common/IconCount";
import PostForm, { PostFormValues } from "./PostForm";

type Props = Post & {
  isAuthorized: boolean,
  isSubmitting: boolean,
  isOwn: boolean,
  editMode: boolean,
  handleEditClick: () => void,
  handleDeleteClick: () => void,
  handleLikeClick: () => void,
  handleCommentsClick: () => void,
  handleUnauthorizedClick: () => void,
  onFinish: (values: PostFormValues) => void,
  cancelButton: JSX.Element
}

const PostComponent: React.FC<Props> = ({ isAuthorized, id, category, author, content, created, isLiked, likesCount, commentsCount, isSubmitting, isOwn, editMode, handleDeleteClick, handleEditClick, handleLikeClick, handleCommentsClick, handleUnauthorizedClick, onFinish, cancelButton }) => {

  if (editMode) {
    return <PostForm onFinish={onFinish} initialValues={{ category, content }} extraComponents={[cancelButton]} />
  }

  return <List.Item key={id}
    actions={[
      <IconCount
        icon={isLiked ? LikeFilled : LikeOutlined}
        count={likesCount}
        onClick={isAuthorized ? handleLikeClick : handleUnauthorizedClick}
        messageId={isLiked ? "buttons.unlike" : "buttons.like"}
        defaultMessage={isLiked ? "unlike" : "like"}
        isSubmitting={isSubmitting}
      />,
      <IconCount
        icon={MessageOutlined}
        count={commentsCount}
        onClick={isAuthorized ? handleCommentsClick : handleUnauthorizedClick}
        messageId="buttons.view-comments"
        defaultMessage="view comments"
      />,
      isOwn ? <Button onClick={handleEditClick}>
        <FormattedMessage
          id="buttons.edit"
          defaultMessage="edit"
        />
      </Button> : <div />,
      isOwn ? <Button onClick={handleDeleteClick}>
        <FormattedMessage
          id="buttons.delete"
          defaultMessage="delete"
        />
      </Button> : <div />
    ]}
  >
    <List.Item.Meta
      title={<NavLink to={"/users/" + author.id}>{author.login}</NavLink>}
      avatar={<NavLink to={"/users/" + author.id}><Avatar src={author.photoUrl} /></NavLink>}
      description={
        <FormattedDate
          value={created}
          year="numeric"
          month="long"
          day="numeric"
        />
      }
    />
    {content}
  </List.Item>
}

export default PostComponent;