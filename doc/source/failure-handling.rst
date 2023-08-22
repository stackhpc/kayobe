================
Failure Handling
================

To cover:

* overview of failure handling
* specifics of ansible behaviour?
* stats plugin, how to enable it
* --continue-on-unreachable
* Supported commands
* Reporting

Overview
========

This section describes how failures are handled in Kayobe, as well as some
techniques for graceful handling of unreachable hosts.

Ansible behaviour
=================

Ansible behaviour is not completely documented, and sometimes it is necessary
to resort to empirical methods to determine how it acts in different
situations. The `ansible-experiments
<https://github.com/markgoddard/ansible-experiments/>`__ repository provides
some examples.

Based on experiment 14, we understand that Ansible will exit non-zero in the
following circumstances:

* all hosts targeted to the current play are marked as failed or
  unreachable, even if there are other hosts in the inventory
* any hosts are marked as failed or unreachable at the end of a top-level
  playbook (specified as a CLI argument)
* any hosts are marked as failed or unreachable in a play or task marked with
  ``any_errors_fatal=true``
* the number of hosts marked as failed or unreachable in a play exceeds the
  ``max_fail_percentage`` (if one is specified)

Kolla stats callback plugin
===========================

The :ansible-collection-kolla-doc:`Kolla Ansible Collection <>` provides a
``openstack.kolla.stats`` callback plugin which may be used to collect
statistics on an Ansible run. Kayobe can make use of this plugin to determine
whether a failure should be treated as fatal or not.

The plugin can be enabled by adding ``openstack.kolla.stats`` to the
``[defaults] callbacks_enabled`` setting in ``ansible.cfg``. See :doc:`here
</configuration/reference/ansible>` for information on configuring Ansible.

Continuing on unreachable hosts
===============================

The following commands support the ``--continue-on-unreachable`` argument:

* ``kayobe kolla ansible run``
* ``kayobe network connectivity check``
* ``kayobe overcloud container image pull``
* ``kayobe overcloud facts gather``
* ``kayobe overcloud host command run``
* ``kayobe overcloud host configure``
* ``kayobe overcloud host package update``
* ``kayobe overcloud host upgrade``
* ``kayobe overcloud service configuration generate``
* ``kayobe overcloud service configuration save``
* ``kayobe overcloud service deploy``
* ``kayobe overcloud service deploy containers``
* ``kayobe overcloud service prechecks``
* ``kayobe overcloud service reconfigure``
* ``kayobe overcloud service stop``
* ``kayobe overcloud service upgrade``
* ``kayobe overcloud service destroy``
* ``kayobe physical network configure``
* ``kayobe playbook run``

Reporting
=========

- Exit codes
- Text output
