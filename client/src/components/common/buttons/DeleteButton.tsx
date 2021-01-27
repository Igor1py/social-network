import React from "react";
import { FormattedMessage } from "react-intl";
import { Button } from "antd";

type Props = {
  onClick: () => void,
  type?: "text" | "link" | "ghost" | "default" | "primary" | "dashed"
}

const DeleteButton: React.FC<Props> = ({ onClick, type = "text" }) => {
  return <Button danger onClick={onClick} type={type}>
    <FormattedMessage id="buttons.delete" />
  </Button>
}

export default DeleteButton;