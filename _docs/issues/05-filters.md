## Goal

Students can filter their private assignment list by subject and completion status, while deadlines are ordered predictably and assignments without dates remain visible.

## Acceptance criteria

- [ ] The list offers All, Not completed, and Completed status filters.
- [ ] An absent/empty status parameter means all; `pending` and `completed` select the matching state.
- [ ] An invalid non-empty status returns a readable 400 response, does not change data, and reveals no other student's assignments.
- [ ] Subject choices are derived only from the current student's assignments and contain an All subjects option.
- [ ] A selected subject matches that exact stored subject value.
- [ ] Absent/empty subject means all subjects.
- [ ] Subject and status filters combine with AND.
- [ ] Selected filter values remain visible in the controls after submission.
- [ ] No matches shows a clear empty-result message and a Clear filters action.
- [ ] Applying or clearing filters never mutates assignment records.
- [ ] Dated assignments come first, in ascending deadline order.
- [ ] Equal dated deadlines are ordered by ascending creation timestamp then primary key.
- [ ] Undated assignments come after dated assignments, in ascending creation timestamp then primary key.
- [ ] Sorting applies consistently to filtered and unfiltered results, including completed entries.
- [ ] Tests with two students prove filtered results and subject options never include the other student's data.
- [ ] Tests cover every status option, subject matching, combined filters, invalid status, no matches, clear filters, mixed null/date ordering, and tied dates.
- [ ] The full suite and Django checks pass with actual evidence in the live issue.

## Out of scope

- Full-text search, pagination, priority, and custom sorting preferences are outside the MVP.
- The status mutation action belongs to the [status task](04-status.md).
- Group-wide subjects and teacher-created tasks are outside the MVP.

Replace draft references with actual issue links after transfer.

## Constraints

- Prerequisite: the [status task](04-status.md) is independently verified and closed.
- Files: assignment list view/queryset, template/styles, and filter/order tests.
- Apply ownership restriction before deriving subject choices or filtering.
- Follow the exact query parameter contract in `_docs/api.md`.
- Use the Django ORM; no new service, dependency, or external data source.
