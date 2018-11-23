import Button, { ButtonProps } from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { withStyles, WithStyles } from "@material-ui/core/styles";
import CheckIcon from "@material-ui/icons/Check";
import classNames from "classnames";
import * as React from "react";

import i18n from "../../i18n";

export type ConfirmButtonTransitionState =
  | "loading"
  | "success"
  | "error"
  | "default";

export interface ConfirmButtonProps extends ButtonProps {
  children: string;
  transitionState: ConfirmButtonTransitionState;
}
interface ConfirmButtonState {
  displayCompletedActionState: boolean;
}

const decorate = withStyles(theme => ({
  error: {
    "&:hover": {
      backgroundColor: theme.palette.error.main
    },
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText
  },
  icon: {
    marginLeft: "0 !important",
    position: "absolute" as "absolute",
    transitionDuration: theme.transitions.duration.standard + "ms"
  },
  invisible: {
    opacity: 0
  },
  label: {
    transitionDuration: theme.transitions.duration.standard + "ms"
  },
  progress: {
    "& svg": {
      color: theme.palette.common.white,
      margin: 0
    },
    position: "absolute" as "absolute",
    transitionDuration: theme.transitions.duration.standard + "ms"
  },
  success: {
    "&:hover": {
      backgroundColor: theme.palette.primary.main
    },
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText
  }
}));
const ConfirmButton = decorate<ConfirmButtonProps>(
  class ConfirmButtonComponent extends React.Component<
    ConfirmButtonProps &
      WithStyles<
        "error" | "icon" | "invisible" | "label" | "progress" | "success"
      >,
    ConfirmButtonState
  > {
    static getDerivedStateFromProps(
      nextProps: ConfirmButtonProps
    ): ConfirmButtonState {
      if (nextProps.transitionState === "loading") {
        return {
          displayCompletedActionState: true
        };
      }
    }

    state: ConfirmButtonState = {
      displayCompletedActionState: false
    };
    timeout = null;

    componentDidUpdate(prevProps: ConfirmButtonProps) {
      const { transitionState } = this.props;
      if (prevProps.transitionState !== transitionState) {
        if (
          (["error", "success"] as ConfirmButtonTransitionState[]).includes(
            transitionState
          )
        ) {
          this.timeout = setTimeout(
            () =>
              this.setState({
                displayCompletedActionState: false
              }),
            2000
          );
        } else if (transitionState === "loading") {
          clearTimeout(this.timeout);
        }
      }
    }

    componentWillUnmount() {
      clearTimeout(this.timeout);
    }

    render() {
      const {
        children,
        classes,
        className,
        disabled,
        transitionState,
        onClick,
        ...props
      } = this.props;
      const { displayCompletedActionState } = this.state;

      return (
        <Button
          variant="contained"
          onClick={transitionState === "loading" ? undefined : onClick}
          color="secondary"
          className={classNames({
            [classes.error]:
              transitionState === "error" && displayCompletedActionState,
            [classes.success]:
              transitionState === "success" && displayCompletedActionState,
            [className]: true
          })}
          disabled={!displayCompletedActionState && disabled}
          {...props}
        >
          <CircularProgress
            size={24}
            color="inherit"
            className={classNames({
              [classes.progress]: true,
              [classes.invisible]: transitionState !== "loading"
            })}
          />
          <CheckIcon
            className={classNames({
              [classes.icon]: true,
              [classes.invisible]: !(
                transitionState === "success" && displayCompletedActionState
              )
            })}
          />
          <span
            className={classNames({
              [classes.label]: true,
              [classes.invisible]:
                (transitionState === "loading" ||
                  transitionState === "success") &&
                displayCompletedActionState
            })}
          >
            {transitionState === "error" && displayCompletedActionState
              ? i18n.t("Error", {
                  context: "button"
                })
              : children ||
                i18n.t("Confirm", {
                  context: "button"
                })}
          </span>
        </Button>
      );
    }
  }
);
ConfirmButton.displayName = "ConfirmButton";
export default ConfirmButton;
