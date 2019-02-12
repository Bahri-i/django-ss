import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import TextField from "@material-ui/core/TextField";
import * as React from "react";

import CardTitle from "../../../components/CardTitle";
import i18n from "../../../i18n";
import { FormData } from "../PageDetailsPage";

export interface PageSlugProps {
  data: FormData;
  disabled: boolean;
  errors: Partial<Record<"slug", string>>;
  onChange: (event: React.ChangeEvent<any>) => void;
}

const PageSlug: React.StatelessComponent<PageSlugProps> = ({
  data,
  disabled,
  errors,
  onChange
}) => (
  <Card>
    <CardTitle title={i18n.t("URL")} />
    <CardContent>
      <TextField
        name={"slug" as keyof FormData}
        disabled={disabled}
        label={i18n.t("Slug")}
        helperText={
          errors.slug ||
          i18n.t("If empty, URL will be autogenerated from Page Name")
        }
        placeholder={data.title.toLowerCase()}
        value={data.slug}
        onChange={onChange}
      />
    </CardContent>
  </Card>
);
PageSlug.displayName = "PageSlug";
export default PageSlug;
