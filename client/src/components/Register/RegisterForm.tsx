import React, { useState } from "react";
import usersAPI from "../../api/users";
import { FormattedMessage } from "react-intl";
import { Form, Input, Button, Checkbox } from 'antd';

type RegisterFormValues = {
  login: string,
  password: string
}

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const LoginForm: React.FC = () => {

  let [isSubmitting, setSubmitting] = useState(false);

  const onFinish = async (values: RegisterFormValues) => {
    setSubmitting(true);
    try {
      const data = await usersAPI.register(values.login, values.password);
      console.log(data);
    } catch {}
    setSubmitting(false);
  };

  return <Form
    {...layout}
    initialValues={{ login: "", password: "" }}
    onFinish={onFinish}
  >

    <Form.Item name="login"
      label={<FormattedMessage id="login" defaultMessage="login" />}
      rules={[
        {
          required: true,
          message: <FormattedMessage id="empty-login" defaultMessage="empty login" />
        }
      ]}
    ><Input /></Form.Item>

    <Form.Item name="password"
      label={<FormattedMessage id="password" defaultMessage="password" />}
      rules={[
        {
          required: true,
          message: <FormattedMessage id="empty-password" defaultMessage="empty password" />
        }
      ]}
    ><Input.Password /></Form.Item>

    <Form.Item {...tailLayout}>
      <Button type="primary" htmlType="submit" disabled={isSubmitting}>
        <FormattedMessage id="buttons.sign-in" defaultMessage="sign in" />
      </Button>
    </Form.Item>

  </Form>
}

export default React.memo(LoginForm);