const ROOT = "../saleor/static/dashboard-next";

const componentGeneratorConfig = {
  description: "New component",
  prompts: [
    {
      type: "input",
      name: "name",
      message: "Name"
    },
    {
      type: "input",
      name: "section",
      message: "Section"
    },
    {
      type: "confirm",
      name: "fc",
      message: "Is it a functional component?",
      default: "y"
    },
    {
      type: "confirm",
      name: "styled",
      message: "Is it a styled component?",
      default: "y"
    },
    {
      type: "confirm",
      name: "story",
      message: "Create story?",
      default: "y"
    }
  ],
  actions: ({ fc, story }) => {
    const actions = [
      {
        type: "add",
        path: `${ROOT}/{{ section }}/{{ name }}/index.ts`,
        templateFile: './component/index.ts.hbs',
        abortOnFail: true
      },
      {
        type: "add",
        path: `${ROOT}/{{ section }}/{{ name }}/{{ name }}.tsx`,
        templateFile: fc
          ? "./component/componentName.fc.tsx.hbs"
          : "./component/componentName.class.tsx.hbs",
        abortOnFail: true
      },
    ];

    if (story) {
      actions.push({
        type: "add",
        path: `${ROOT}/storybook/stories/{{ section }}/{{ name }}.tsx`,
        templateFile: "./component/componentName.story.tsx.hbs",
        abortOnFail: true
      });
    }

    return actions;
  }
};

module.exports = plop => {
  plop.setGenerator('component', componentGeneratorConfig);
};
