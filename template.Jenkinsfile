@Library('diag-pipeline') _

diag_build([
  'diagioc_fths': [
    deployed_as: 'fths',
    top_dir: '.',
    auto_restart: false,
    deb_packages: [
      'epics-asyn-dev',
      'epics-stream-dev',
      'epics-pydevsup-dev',
      'python3-xlrd',
    ],
    instances: [
{%- for item in the_names %}
      'ioc-{{ item }}',
{%- endfor %}
    ]
  ]
])
