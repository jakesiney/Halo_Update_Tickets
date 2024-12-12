SELECT faultid AS [Ticket ID],
    (SELECT aareadesc FROM area WHERE aarea = areaint) AS [Client],
    (SELECT sdesc FROM site WHERE ssitenum = sitenumber) AS [Site],
    FIsBillable as [Billable],
    username AS [User],
    symptom AS [Summary],
    FResponseDate as [First Response],
    dateoccured AS [Date Opened],
    datecleared AS [Date Closed],
    CONVERT(VARCHAR(10), DATEDIFF(MINUTE, dateoccured, datecleared) / 1440) + ' days ' 
    + CONVERT(VARCHAR(5), (DATEDIFF(MINUTE, dateoccured, datecleared) % 1440) / 60) + ' hours ' 
    + CONVERT(VARCHAR(2), DATEDIFF(MINUTE, dateoccured, datecleared) % 60) + ' mins' AS [Total Time],
    (SELECT tstatusdesc FROM tstatus WHERE tstatus = status) AS [Status],
    (SELECT uname FROM uname WHERE unum = assignedtoint) AS [Technician],
    sectio_ AS [Section],
    (SELECT rtdesc FROM requesttype WHERE rtid = requesttypenew) AS [Request type],
    category2 AS [Category],
    category3 AS [Category 2],
    category4 AS [Category 3],
    category5 AS [Category 4],
    (SELECT pdesc FROM policy WHERE ppolicy = seriousness AND pslaid = slaid) AS [Priority],
    (SELECT sldesc FROM slahead WHERE slid = slaid) AS [SLA],
    slastate AS [Resolution State],
    slaresponsestate AS [Response State],
    CASE WHEN slastate = 'I' AND slaresponsestate = 'I' THEN 'Passed' ELSE 'Failed' END AS [SLA Result],
    satisfactionlevel AS [Survey Level],
    (SELECT uname FROM uname WHERE unum = clearwhoint) AS [Closed By],
    (SELECT fvalue FROM lookup WHERE fcode = frequestsource AND fid = 22) AS [Ticket Source],
    (select fvalue from lookup where fid = 135 and fcode = CFCFTicketResolution) as [Resolution]
FROM faults
WHERE fdeleted = 0 AND Symptom not like 'Quick Time - %'

