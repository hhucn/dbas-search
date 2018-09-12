select
  stat.uid,
  stat.is_position,
  txt.content,
  txt.author_uid,
  usr.public_nickname,
  iss.uid as issue_uid,
  iss.slug,
  lang.ui_locales,
  iss.title,
  iss.info
from public.statements as stat,
  public.textversions as txt,
  public.users as usr,
  public.statement_to_issue as sti,
  public.issues as iss,
  public.languages as lang
where stat.uid = {0}
and usr.uid = {1}
and stat.uid = txt.statement_uid
and usr.uid = txt.author_uid
and stat.uid = sti.statement_uid
and iss.uid = sti.issue_uid
and iss.lang_uid = lang.uid