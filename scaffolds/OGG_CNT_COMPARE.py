# -*- coding:utf-8 -*-  
__author__ = 'bowenz'
'''
  compare oracle OGG count between source and target 
'''
import sys
import threading
import Queue
import cx_Oracle
import collections
import copy
import json

q = Queue.Queue()


def get_cnt(cur, tbl_name, source_name):
    query = 'select count(*) from %s' % tbl_name
    res = cur.execute(query)
    cnt = res.fetchone()[0]
    q.put((source_name, tbl_name, cnt))


def main(source1, source1_name, source2, source2_name, source3, source3_name, source1_tbl, source2_tbl, source3_tbl):
    result = collections.OrderedDict()
    # cur1 = cx_Oracle.connect('%s' % source1).cursor()
    cur2 = cx_Oracle.connect('%s' % source2).cursor()
    cur3 = cx_Oracle.connect('%s' % source3).cursor()
    # t1 = threading.Thread(target=get_cnt, name='query1', args=(cur1, source1_tbl, source1_name,))
    t2 = threading.Thread(target=get_cnt, name='query2', args=(cur2, source2_tbl, source2_name,))
    t3 = threading.Thread(target=get_cnt, name='query3', args=(cur3, source3_tbl, source3_name,))
    # t1.start()
    t2.start()
    t3.start()
    # t1.join()
    t2.join()
    t3.join()
    while not q.empty():
        source_name, table_name, cnt = q.get()
        result[("%s.%s") % (source_name, table_name)] = cnt
    result2 = copy.deepcopy(result)
    first_key = "none"
    second_key = "none"
    for i, key in enumerate(result.keys()):
        if i == 0:
            first_key = key
        elif i == 1:
            second_key = key
        if i > 0:
            cntdiff = result[key] - result[first_key]
            result2[('DIFF %s --> %s') % (first_key.split('.')[0], key.split('.')[0])] = cntdiff
            # if i > 1:
            #     cntdiff = result[key] - result[second_key]
            #     result2[('DIFF %s --> %s') % (second_key.split('.')[0], key.split('.')[0])] = cntdiff

    print(json.dumps(result2))


if __name__ == '__main__':
    # print "+++++++++rrs ogg to dwprod++++++++++"
    # source1 = 'system/xxxxxxxxxxxxxxxx@sjprdwdb01/SJDWPROD'
    # source1_name = 'old_dwprod'
    # source2 = 'system/xxxxxxxxxxxxxxxx@sjprdwdb06/PDWPROD'
    # source2_name = 'new_dwprod'
    # source3 = 'system/xxxxxxxxxxxxxxxx@sjprrrsdb01/SJRRSPROD'
    # source3_name = 'rrsprod'
    # tables = [
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_CARRIER', 'ods_pr_rrs_ora_rrsadmin.RRS_CARRIER', 'rrsadmin.RRS_CARRIER'),
    #     ('ods_pr_rrs_ora_rrsadmin.BO_POLICY_CHANGE_LIST', 'ods_pr_rrs_ora_rrsadmin.BO_POLICY_CHANGE_LIST',
    #      'rrsadmin.BO_POLICY_CHANGE_LIST'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_CATEGORY_CLASS', 'ods_pr_rrs_ora_rrsadmin.RRS_CATEGORY_CLASS',
    #      'rrsadmin.RRS_CATEGORY_CLASS'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_CHECK', 'ods_pr_rrs_ora_rrsadmin.RRS_CHECK', 'rrsadmin.RRS_CHECK'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_DELETED_RECORDS', 'ods_pr_rrs_ora_rrsadmin.RRS_DELETED_RECORDS',
    #      'rrsadmin.RRS_DELETED_RECORDS'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_INVOICE', 'ods_pr_rrs_ora_rrsadmin.RRS_INVOICE', 'rrsadmin.RRS_INVOICE'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_ARCHIVE', 'ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_ARCHIVE',
    #      'rrsadmin.RRS_INVOICE_ARCHIVE'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_BALANCE', 'ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_BALANCE',
    #      'rrsadmin.RRS_INVOICE_BALANCE'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_BALANCE_ARCHIVE',
    #      'ods_pr_rrs_ora_rrsadmin.RRS_INVOICE_BALANCE_ARCHIVE', 'rrsadmin.RRS_INVOICE_BALANCE_ARCHIVE'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_ITEM', 'ods_pr_rrs_ora_rrsadmin.RRS_ITEM', 'rrsadmin.RRS_ITEM'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_PERIOD', 'ods_pr_rrs_ora_rrsadmin.RRS_PERIOD', 'rrsadmin.RRS_PERIOD'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_PLAN', 'ods_pr_rrs_ora_rrsadmin.RRS_PLAN', 'rrsadmin.RRS_PLAN'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_POLICY_HISTORY', 'ods_pr_rrs_ora_rrsadmin.RRS_POLICY_HISTORY',
    #      'rrsadmin.RRS_POLICY_HISTORY'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_POLICY_MEMBER', 'ods_pr_rrs_ora_rrsadmin.RRS_POLICY_MEMBER',
    #      'rrsadmin.RRS_POLICY_MEMBER'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_RIDER', 'ods_pr_rrs_ora_rrsadmin.RRS_RIDER', 'rrsadmin.RRS_RIDER'),
    #     ('ods_pr_rrs_ora_rrsadmin.RRS_UNEARNED', 'ods_pr_rrs_ora_rrsadmin.RRS_UNEARNED', 'rrsadmin.RRS_UNEARNED')
    # ]
    # for tbl_name in tables:
    #     main(source1, source1_name, source2, source2_name, source3, source3_name,
    #          tbl_name[0], tbl_name[1], tbl_name[2])
    print "+++++++++ehi ogg to dwprod++++++++++"
    source1 = 'system/xxxxxxxxxxxxxxxx@sjprdwdb01/SJDWPROD'
    source1_name = 'old_dwprod'
    source2 = 'system/xxxxxxxxxxxxxxxx@sjprdwdb06/PDWPROD'
    source2_name = 'new_dwprod'
    source3 = 'ehquery/xxxxxxxxxxxxxxxx@sjprdb05/SJPROD'
    source3_name = 'ehi_prod'
    tables = [
        ('ods_pr_ehi_ora_ehadmin.AGENT', 'ods_pr_ehi_ora_ehadmin.AGENT', 'ehadmin.AGENT'),
        ('ods_pr_ehi_ora_ehadmin.AGENT_CARRIER_LICENSE', 'ods_pr_ehi_ora_ehadmin.AGENT_CARRIER_LICENSE',
         'ehadmin.AGENT_CARRIER_LICENSE'),
        ('ods_pr_ehi_ora_ehadmin.AGENT_CUSTOMER_PROFILE', 'ods_pr_ehi_ora_ehadmin.AGENT_CUSTOMER_PROFILE',
         'ehadmin.AGENT_CUSTOMER_PROFILE'),
        ('ods_pr_ehi_ora_ehadmin.AGENT_PARTNERSHIP', 'ods_pr_ehi_ora_ehadmin.AGENT_PARTNERSHIP',
         'ehadmin.AGENT_PARTNERSHIP'),
        ('ods_pr_ehi_ora_ehadmin.AGENT_STATE_OF_LICENSURE', 'ods_pr_ehi_ora_ehadmin.AGENT_STATE_OF_LICENSURE',
         'ehadmin.AGENT_STATE_OF_LICENSURE'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_CARRIER', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_CARRIER',
         'ehadmin.ALLIANCE_CARRIER'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_CATEGORY', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_CATEGORY',
         'ehadmin.ALLIANCE_CATEGORY'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_INFORMATION', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_INFORMATION',
         'ehadmin.ALLIANCE_INFORMATION'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_PHONE', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_PHONE', 'ehadmin.ALLIANCE_PHONE'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_PRODUCTLINE', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_PRODUCTLINE',
         'ehadmin.ALLIANCE_PRODUCTLINE'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION', 'ods_pr_ehi_ora_ehadmin.APPLICATION', 'ehadmin.APPLICATION'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION_AGENT', 'ods_pr_ehi_ora_ehadmin.APPLICATION_AGENT',
         'ehadmin.APPLICATION_AGENT'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION_EXTENSION', 'ods_pr_ehi_ora_ehadmin.APPLICATION_EXTENSION',
         'ehadmin.APPLICATION_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION_PROCESS', 'ods_pr_ehi_ora_ehadmin.APPLICATION_PROCESS',
         'ehadmin.APPLICATION_PROCESS'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION_STATUS', 'ods_pr_ehi_ora_ehadmin.APPLICATION_STATUS',
         'ehadmin.APPLICATION_STATUS'),
        ('ods_pr_ehi_ora_ehadmin.APPLICATION_TRACKING', 'ods_pr_ehi_ora_ehadmin.APPLICATION_TRACKING',
         'ehadmin.APPLICATION_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.APPOINTMENT', 'ods_pr_ehi_ora_ehadmin.APPOINTMENT', 'ehadmin.APPOINTMENT'),
        ('ods_pr_ehi_ora_ehadmin.APPOINTMENT_APPLICATION', 'ods_pr_ehi_ora_ehadmin.APPOINTMENT_APPLICATION',
         'ehadmin.APPOINTMENT_APPLICATION'),
        ('ods_pr_ehi_ora_ehadmin.APPOINTMENT_LEAD', 'ods_pr_ehi_ora_ehadmin.APPOINTMENT_LEAD',
         'ehadmin.APPOINTMENT_LEAD'),
        ('ods_pr_ehi_ora_ehadmin.APPOINTMENT_SCRIPT_SESSION', 'ods_pr_ehi_ora_ehadmin.APPOINTMENT_SCRIPT_SESSION',
         'ehadmin.APPOINTMENT_SCRIPT_SESSION'),
        ('ods_pr_ehi_ora_ehadmin.APPOINTMENT_SELECTED_PLAN', 'ods_pr_ehi_ora_ehadmin.APPOINTMENT_SELECTED_PLAN',
         'ehadmin.APPOINTMENT_SELECTED_PLAN'),
        ('ods_pr_ehi_ora_ehadmin.BEST_SELLER_SEGMENT', 'ods_pr_ehi_ora_ehadmin.BEST_SELLER_SEGMENT',
         'ehadmin.BEST_SELLER_SEGMENT'),
        ('ods_pr_ehi_ora_ehadmin.BO_CARRIER_MAP', 'ods_pr_ehi_ora_ehadmin.BO_CARRIER_MAP', 'ehadmin.BO_CARRIER_MAP'),
        ('ods_pr_ehi_ora_ehadmin.BO_COMLOG_DOCUMENT_MAP', 'ods_pr_ehi_ora_ehadmin.BO_COMLOG_DOCUMENT_MAP',
         'ehadmin.BO_COMLOG_DOCUMENT_MAP'),
        ('ods_pr_ehi_ora_ehadmin.BO_USER_ALLIANCE_MAP', 'ods_pr_ehi_ora_ehadmin.BO_USER_ALLIANCE_MAP',
         'ehadmin.BO_USER_ALLIANCE_MAP'),
        ('ods_pr_ehi_ora_ehadmin.BO_USER_ROLE_EXTENSION', 'ods_pr_ehi_ora_ehadmin.BO_USER_ROLE_EXTENSION',
         'ehadmin.BO_USER_ROLE_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.BROKER', 'ods_pr_ehi_ora_ehadmin.BROKER', 'ehadmin.BROKER'),
        ('ods_pr_ehi_ora_ehadmin.CARRIER', 'ods_pr_ehi_ora_ehadmin.CARRIER', 'ehadmin.CARRIER'),
        ('ods_pr_ehi_ora_ehadmin.CARRIER_FAMILY', 'ods_pr_ehi_ora_ehadmin.CARRIER_FAMILY', 'ehadmin.CARRIER_FAMILY'),
        ('ods_pr_ehi_ora_ehadmin.CARRIER_REGION', 'ods_pr_ehi_ora_ehadmin.CARRIER_REGION', 'ehadmin.CARRIER_REGION'),
        ('ods_pr_ehi_ora_ehadmin.CUSTOMER_OUTBOUND_INFO', 'ods_pr_ehi_ora_ehadmin.CUSTOMER_OUTBOUND_INFO',
         'ehadmin.CUSTOMER_OUTBOUND_INFO'),
        ('ods_pr_ehi_ora_ehadmin.CUSTOMER_SCRIPT_SESSION', 'ods_pr_ehi_ora_ehadmin.CUSTOMER_SCRIPT_SESSION',
         'ehadmin.CUSTOMER_SCRIPT_SESSION'),
        ('ods_pr_ehi_ora_ehadmin.CX_CAREFIRST_TRANSFER', 'ods_pr_ehi_ora_ehadmin.CX_CAREFIRST_TRANSFER',
         'ehadmin.CX_CAREFIRST_TRANSFER'),
        ('ods_pr_ehi_ora_ehadmin.DOCUMENT', 'ods_pr_ehi_ora_ehadmin.DOCUMENT', 'ehadmin.DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.FAST_QUOTE_VISITOR', 'ods_pr_ehi_ora_ehadmin.FAST_QUOTE_VISITOR',
         'ehadmin.FAST_QUOTE_VISITOR'),
        ('ods_pr_ehi_ora_ehadmin.GENERIC_AUDIT_LOG', 'ods_pr_ehi_ora_ehadmin.GENERIC_AUDIT_LOG',
         'ehadmin.GENERIC_AUDIT_LOG'),
        ('ods_pr_ehi_ora_ehadmin.IFP_PDF_ARCHIVE', 'ods_pr_ehi_ora_ehadmin.IFP_PDF_ARCHIVE', 'ehadmin.IFP_PDF_ARCHIVE'),
        ('ods_pr_ehi_ora_ehadmin.IMAGE_APPLICATION_ASSOCIATION', 'ods_pr_ehi_ora_ehadmin.IMAGE_APPLICATION_ASSOCIATION',
         'ehadmin.IMAGE_APPLICATION_ASSOCIATION'),
        ('ods_pr_ehi_ora_ehadmin.INT_REPORT_LOG', 'ods_pr_ehi_ora_ehadmin.INT_REPORT_LOG', 'ehadmin.INT_REPORT_LOG'),
        ('ods_pr_ehi_ora_ehadmin.INT_STATUS_UPDATE_TRACKING', 'ods_pr_ehi_ora_ehadmin.INT_STATUS_UPDATE_TRACKING',
         'ehadmin.INT_STATUS_UPDATE_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.LEAD', 'ods_pr_ehi_ora_ehadmin.LEAD', 'ehadmin.LEAD'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_ADDRESS', 'ods_pr_ehi_ora_ehadmin.LEAD_ADDRESS', 'ehadmin.LEAD_ADDRESS'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_AUDIT_LOG', 'ods_pr_ehi_ora_ehadmin.LEAD_AUDIT_LOG', 'ehadmin.LEAD_AUDIT_LOG'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_SALES_REP_HISTORY', 'ods_pr_ehi_ora_ehadmin.LEAD_SALES_REP_HISTORY',
         'ehadmin.LEAD_SALES_REP_HISTORY'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_MEMBER', 'ods_pr_ehi_ora_ehadmin.LEAD_MEMBER', 'ehadmin.LEAD_MEMBER'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_PHONE', 'ods_pr_ehi_ora_ehadmin.LEAD_PHONE', 'ehadmin.LEAD_PHONE'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_STATUS', 'ods_pr_ehi_ora_ehadmin.LEAD_STATUS', 'ehadmin.LEAD_STATUS'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_TRACKING', 'ods_pr_ehi_ora_ehadmin.LEAD_TRACKING', 'ehadmin.LEAD_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.MERCHANDISE', 'ods_pr_ehi_ora_ehadmin.MERCHANDISE', 'ehadmin.MERCHANDISE'),
        ('ods_pr_ehi_ora_ehadmin.PARENT_PARTNER', 'ods_pr_ehi_ora_ehadmin.PARENT_PARTNER', 'ehadmin.PARENT_PARTNER'),
        ('ods_pr_ehi_ora_ehadmin.PARENT_PARTNER_ALLIANCE', 'ods_pr_ehi_ora_ehadmin.PARENT_PARTNER_ALLIANCE',
         'ehadmin.PARENT_PARTNER_ALLIANCE'),
        ('ods_pr_ehi_ora_ehadmin.PARENT_PARTNER_PRODUCTTYPE', 'ods_pr_ehi_ora_ehadmin.PARENT_PARTNER_PRODUCTTYPE',
         'ehadmin.PARENT_PARTNER_PRODUCTTYPE'),
        ('ods_pr_ehi_ora_ehadmin.PLAN', 'ods_pr_ehi_ora_ehadmin.PLAN', 'ehadmin.PLAN'),
        ('ods_pr_ehi_ora_ehadmin.PLAN_BENEFIT', 'ods_pr_ehi_ora_ehadmin.PLAN_BENEFIT', 'ehadmin.PLAN_BENEFIT'),
        ('ods_pr_ehi_ora_ehadmin.PLAN_EXTENSION', 'ods_pr_ehi_ora_ehadmin.PLAN_EXTENSION', 'ehadmin.PLAN_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.POLICY', 'ods_pr_ehi_ora_ehadmin.POLICY', 'ehadmin.POLICY'),
        ('ods_pr_ehi_ora_ehadmin.PRODUCT', 'ods_pr_ehi_ora_ehadmin.PRODUCT', 'ehadmin.PRODUCT'),
        ('ods_pr_ehi_ora_ehadmin.PRODUCTLINE', 'ods_pr_ehi_ora_ehadmin.PRODUCTLINE', 'ehadmin.PRODUCTLINE'),
        ('ods_pr_ehi_ora_ehadmin.PRODUCT_CATEGORY', 'ods_pr_ehi_ora_ehadmin.PRODUCT_CATEGORY',
         'ehadmin.PRODUCT_CATEGORY'),
        ('ods_pr_ehi_ora_ehadmin.PRODUCT_RATE', 'ods_pr_ehi_ora_ehadmin.PRODUCT_RATE', 'ehadmin.PRODUCT_RATE'),
        ('ods_pr_ehi_ora_ehadmin.PROPOSAL', 'ods_pr_ehi_ora_ehadmin.PROPOSAL', 'ehadmin.PROPOSAL'),
        ('ods_pr_ehi_ora_ehadmin.PROPOSAL_STATUS', 'ods_pr_ehi_ora_ehadmin.PROPOSAL_STATUS', 'ehadmin.PROPOSAL_STATUS'),
        ('ods_pr_ehi_ora_ehadmin.PROPOSAL_TRACKING', 'ods_pr_ehi_ora_ehadmin.PROPOSAL_TRACKING',
         'ehadmin.PROPOSAL_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.RIDER', 'ods_pr_ehi_ora_ehadmin.RIDER', 'ehadmin.RIDER'),
        ('ods_pr_ehi_ora_ehadmin.SELECTED_RIDERS', 'ods_pr_ehi_ora_ehadmin.SELECTED_RIDERS', 'ehadmin.SELECTED_RIDERS'),
        ('ods_pr_ehi_ora_ehadmin.SG_CARRIER', 'ods_pr_ehi_ora_ehadmin.SG_CARRIER', 'ehadmin.SG_CARRIER'),
        ('ods_pr_ehi_ora_ehadmin.SG_CARRIER_REGION', 'ods_pr_ehi_ora_ehadmin.SG_CARRIER_REGION',
         'ehadmin.SG_CARRIER_REGION'),
        ('ods_pr_ehi_ora_ehadmin.SG_GROUP', 'ods_pr_ehi_ora_ehadmin.SG_GROUP', 'ehadmin.SG_GROUP'),
        ('ods_pr_ehi_ora_ehadmin.SG_GROUP_ADDRESS', 'ods_pr_ehi_ora_ehadmin.SG_GROUP_ADDRESS',
         'ehadmin.SG_GROUP_ADDRESS'),
        ('ods_pr_ehi_ora_ehadmin.SG_GROUP_CONTACT', 'ods_pr_ehi_ora_ehadmin.SG_GROUP_CONTACT',
         'ehadmin.SG_GROUP_CONTACT'),
        ('ods_pr_ehi_ora_ehadmin.SG_INSURANCE_TYPE', 'ods_pr_ehi_ora_ehadmin.SG_INSURANCE_TYPE',
         'ehadmin.SG_INSURANCE_TYPE'),
        ('ods_pr_ehi_ora_ehadmin.SG_PLAN', 'ods_pr_ehi_ora_ehadmin.SG_PLAN', 'ehadmin.SG_PLAN'),
        ('ods_pr_ehi_ora_ehadmin.SG_PRODUCT_CATEGORY', 'ods_pr_ehi_ora_ehadmin.SG_PRODUCT_CATEGORY',
         'ehadmin.SG_PRODUCT_CATEGORY'),
        ('ods_pr_ehi_ora_ehadmin.SG_REQUEST_TRACKING', 'ods_pr_ehi_ora_ehadmin.SG_REQUEST_TRACKING',
         'ehadmin.SG_REQUEST_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.SG_SELECTED_PLANS', 'ods_pr_ehi_ora_ehadmin.SG_SELECTED_PLANS',
         'ehadmin.SG_SELECTED_PLANS'),
        ('ods_pr_ehi_ora_ehadmin.SPONSORED_ATTRIBUTE_VALUES', 'ods_pr_ehi_ora_ehadmin.SPONSORED_ATTRIBUTE_VALUES',
         'ehadmin.SPONSORED_ATTRIBUTE_VALUES'),
        ('ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_CARRIER', 'ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_CARRIER',
         'ehadmin.SPONSORED_PROGRAM_CARRIER'),
        ('ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_PLAN', 'ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_PLAN',
         'ehadmin.SPONSORED_PROGRAM_PLAN'),
        ('ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_REGION', 'ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM_REGION',
         'ehadmin.SPONSORED_PROGRAM_REGION'),
        ('ods_pr_ehi_ora_ehadmin.STATE', 'ods_pr_ehi_ora_ehadmin.STATE', 'ehadmin.STATE'),
        ('ods_pr_ehi_ora_ehadmin.UM_ORGANIZATION', 'ods_pr_ehi_ora_ehadmin.UM_ORGANIZATION', 'ehadmin.UM_ORGANIZATION'),
        ('ods_pr_ehi_ora_ehadmin.UM_USER', 'ods_pr_ehi_ora_ehadmin.UM_USER', 'ehadmin.UM_USER'),
        ('ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_DATA', 'ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_DATA',
         'ehadmin.USER_FEEDBACK_DATA'),
        ('ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_INFORMATION', 'ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_INFORMATION',
         'ehadmin.USER_FEEDBACK_INFORMATION'),
        ('ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_MEMBER', 'ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_MEMBER',
         'ehadmin.USER_FEEDBACK_MEMBER'),
        ('ods_pr_ehi_ora_ehadmin.USER_PROFILE', 'ods_pr_ehi_ora_ehadmin.USER_PROFILE', 'ehadmin.USER_PROFILE'),
        ('ods_pr_ehi_ora_ehadmin.USER_REVIEW', 'ods_pr_ehi_ora_ehadmin.USER_REVIEW', 'ehadmin.USER_REVIEW'),
        ('ods_pr_ehi_ora_ehadmin.USER_REVIEW_RATINGS', 'ods_pr_ehi_ora_ehadmin.USER_REVIEW_RATINGS',
         'ehadmin.USER_REVIEW_RATINGS'),
        ('ods_pr_ehi_ora_ehadmin.USER_ROLE', 'ods_pr_ehi_ora_ehadmin.USER_ROLE', 'ehadmin.USER_ROLE'),
        ('ods_pr_ehi_ora_ehadmin.ZIP_REPOSITORY_BASE', 'ods_pr_ehi_ora_ehadmin.ZIP_REPOSITORY_BASE',
         'ehadmin.ZIP_REPOSITORY_BASE'),
        ('ods_pr_ehi_ora_ehadmin.BO_BULK_EMAIL', 'ods_pr_ehi_ora_ehadmin.BO_BULK_EMAIL', 'ehadmin.BO_BULK_EMAIL'),
        ('ods_pr_ehi_ora_ehadmin.AM_BEST_RATINGS', 'ods_pr_ehi_ora_ehadmin.AM_BEST_RATINGS', 'ehadmin.AM_BEST_RATINGS'),
        ('ods_pr_ehi_ora_ehadmin.BO_DOCUMENT_MAP', 'ods_pr_ehi_ora_ehadmin.BO_DOCUMENT_MAP', 'ehadmin.BO_DOCUMENT_MAP'),
        ('ods_pr_ehi_ora_ehadmin.INT_REPORT', 'ods_pr_ehi_ora_ehadmin.INT_REPORT', 'ehadmin.INT_REPORT'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_DOCUMENT', 'ods_pr_ehi_ora_ehadmin.LEAD_DOCUMENT', 'ehadmin.LEAD_DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.POLICY_HISTORY_UPDATED_REASON', 'ods_pr_ehi_ora_ehadmin.POLICY_HISTORY_UPDATED_REASON',
         'ehadmin.POLICY_HISTORY_UPDATED_REASON'),
        ('ods_pr_ehi_ora_ehadmin.SELECTED_PLANS', 'ods_pr_ehi_ora_ehadmin.SELECTED_PLANS', 'ehadmin.SELECTED_PLANS'),
        ('ods_pr_ehi_ora_ehadmin.SG_GROUP_TRACKING', 'ods_pr_ehi_ora_ehadmin.SG_GROUP_TRACKING',
         'ehadmin.SG_GROUP_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM', 'ods_pr_ehi_ora_ehadmin.SPONSORED_PROGRAM',
         'ehadmin.SPONSORED_PROGRAM'),
        ('ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_ANSWER', 'ods_pr_ehi_ora_ehadmin.USER_FEEDBACK_ANSWER',
         'ehadmin.USER_FEEDBACK_ANSWER'),
        ('ods_pr_ehi_ora_ehadmin.WORK_QUEUE', 'ods_pr_ehi_ora_ehadmin.WORK_QUEUE', 'ehadmin.WORK_QUEUE'),
        ('ods_pr_ehi_ora_ehadmin.SG_POLICY_HISTORY', 'ods_pr_ehi_ora_ehadmin.SG_POLICY_HISTORY',
         'ehadmin.SG_POLICY_HISTORY'),
        ('ods_pr_ehi_ora_ehadmin.SG_SELECTED_RIDERS', 'ods_pr_ehi_ora_ehadmin.SG_SELECTED_RIDERS',
         'ehadmin.SG_SELECTED_RIDERS'),
        ('ods_pr_ehi_ora_ehadmin.POLICY_HISTORY', 'ods_pr_ehi_ora_ehadmin.POLICY_HISTORY', 'ehadmin.POLICY_HISTORY'),
        ('ods_pr_ehi_ora_ehadmin.SG_WORK_QUEUE_DOCUMENT', 'ods_pr_ehi_ora_ehadmin.SG_WORK_QUEUE_DOCUMENT',
         'ehadmin.SG_WORK_QUEUE_DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.SG_WORK_QUEUE', 'ods_pr_ehi_ora_ehadmin.SG_WORK_QUEUE', 'ehadmin.SG_WORK_QUEUE'),
        ('ods_pr_ehi_ora_ehadmin.SG_EE_PLAN_EVALUATE_RATE', 'ods_pr_ehi_ora_ehadmin.SG_EE_PLAN_EVALUATE_RATE',
         'ehadmin.SG_EE_PLAN_EVALUATE_RATE'),
        ('ods_pr_ehi_ora_ehadmin.SG_APPLICATION_SEARCH', 'ods_pr_ehi_ora_ehadmin.SG_APPLICATION_SEARCH',
         'ehadmin.SG_APPLICATION_SEARCH'),
        ('ods_pr_ehi_ora_ehadmin.SG_COMPARABLE_PLANS', 'ods_pr_ehi_ora_ehadmin.SG_COMPARABLE_PLANS',
         'ehadmin.SG_COMPARABLE_PLANS'),
        ('ods_pr_ehi_ora_ehadmin.BO_AUTO_MESSAGE', 'ods_pr_ehi_ora_ehadmin.BO_AUTO_MESSAGE', 'ehadmin.BO_AUTO_MESSAGE'),
        ('ods_pr_ehi_ora_ehadmin.SG_PLAN_BENEFIT', 'ods_pr_ehi_ora_ehadmin.SG_PLAN_BENEFIT', 'ehadmin.SG_PLAN_BENEFIT'),
        ('ods_pr_ehi_ora_ehadmin.ALLIANCE_AUDIT_LOG', 'ods_pr_ehi_ora_ehadmin.ALLIANCE_AUDIT_LOG',
         'ehadmin.ALLIANCE_AUDIT_LOG'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_WORK_QUEUE_DOCUMENT', 'ods_pr_ehi_ora_ehadmin.LEAD_WORK_QUEUE_DOCUMENT',
         'ehadmin.LEAD_WORK_QUEUE_DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.SG_APP_TRACKING', 'ods_pr_ehi_ora_ehadmin.SG_APP_TRACKING', 'ehadmin.SG_APP_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.BO_CARRIER_FAMILY_LICENSE_TOOL',
         'ods_pr_ehi_ora_ehadmin.BO_CARRIER_FAMILY_LICENSE_TOOL', 'ehadmin.BO_CARRIER_FAMILY_LICENSE_TOOL'),
        ('ods_pr_ehi_ora_ehadmin.MC_SALES_CARRIER_CERTIFY', 'ods_pr_ehi_ora_ehadmin.MC_SALES_CARRIER_CERTIFY',
         'ehadmin.MC_SALES_CARRIER_CERTIFY'),
        ('ods_pr_ehi_ora_ehadmin.MC_SALES_STATE_APPOINT', 'ods_pr_ehi_ora_ehadmin.MC_SALES_STATE_APPOINT',
         'ehadmin.MC_SALES_STATE_APPOINT'),
        ('ods_pr_ehi_ora_ehadmin.MC_SALES_CARRIER_LICENSE', 'ods_pr_ehi_ora_ehadmin.MC_SALES_CARRIER_LICENSE',
         'ehadmin.MC_SALES_CARRIER_LICENSE'),
        ('ods_pr_ehi_ora_ehadmin.SG_APPLICATION_PROCESS', 'ods_pr_ehi_ora_ehadmin.SG_APPLICATION_PROCESS',
         'ehadmin.SG_APPLICATION_PROCESS'),
        ('ods_pr_ehi_ora_ehadmin.SG_EE_APPLICATION', 'ods_pr_ehi_ora_ehadmin.SG_EE_APPLICATION',
         'ehadmin.SG_EE_APPLICATION'),
        ('ods_pr_ehi_ora_ehadmin.UM_ORGANIZATION_CARRIER_FAMILY',
         'ods_pr_ehi_ora_ehadmin.UM_ORGANIZATION_CARRIER_FAMILY', 'ehadmin.UM_ORGANIZATION_CARRIER_FAMILY'),
        ('ods_pr_ehi_ora_ehadmin.WBE_APPLICATION_EXTENSION', 'ods_pr_ehi_ora_ehadmin.WBE_APPLICATION_EXTENSION',
         'ehadmin.WBE_APPLICATION_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.SG_APPLICATION_EXTENSION', 'ods_pr_ehi_ora_ehadmin.SG_APPLICATION_EXTENSION',
         'ehadmin.SG_APPLICATION_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.SG_RIDER', 'ods_pr_ehi_ora_ehadmin.SG_RIDER', 'ehadmin.SG_RIDER'),
        ('ods_pr_ehi_ora_ehadmin.PE_COMPANY_TRACKING', 'ods_pr_ehi_ora_ehadmin.PE_COMPANY_TRACKING',
         'ehadmin.PE_COMPANY_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.PE_APPLICATION_EXTENSION', 'ods_pr_ehi_ora_ehadmin.PE_APPLICATION_EXTENSION',
         'ehadmin.PE_APPLICATION_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.PE_COMPANY', 'ods_pr_ehi_ora_ehadmin.PE_COMPANY', 'ehadmin.PE_COMPANY'),
        ('ods_pr_ehi_ora_ehadmin.CALL_DISPOSITION', 'ods_pr_ehi_ora_ehadmin.CALL_DISPOSITION',
         'ehadmin.CALL_DISPOSITION'),
        ('ods_pr_ehi_ora_ehadmin.SG_GROUP_STATUS', 'ods_pr_ehi_ora_ehadmin.SG_GROUP_STATUS', 'ehadmin.SG_GROUP_STATUS'),
        ('ods_pr_ehi_ora_ehadmin.SG_MEMBER_ENROLLMENT_SELECTION',
         'ods_pr_ehi_ora_ehadmin.SG_MEMBER_ENROLLMENT_SELECTION', 'ehadmin.SG_MEMBER_ENROLLMENT_SELECTION'),
        ('ods_pr_ehi_ora_ehadmin.SG_EMPLOYEE', 'ods_pr_ehi_ora_ehadmin.SG_EMPLOYEE', 'ehadmin.SG_EMPLOYEE'),
        ('ods_pr_ehi_ora_ehadmin.POLICY_MEMBER', 'ods_pr_ehi_ora_ehadmin.POLICY_MEMBER', 'ehadmin.POLICY_MEMBER'),
        ('ods_pr_ehi_ora_ehadmin.AUDIT_TRACKING', 'ods_pr_ehi_ora_ehadmin.AUDIT_TRACKING', 'ehadmin.AUDIT_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_SEARCH', 'ods_pr_ehi_ora_ehadmin.LEAD_SEARCH', 'ehadmin.LEAD_SEARCH'),
        ('ods_pr_ehi_ora_ehadmin.MC_USER_PROFILE_EXTENSION', 'ods_pr_ehi_ora_ehadmin.MC_USER_PROFILE_EXTENSION',
         'ehadmin.MC_USER_PROFILE_EXTENSION'),
        ('ods_pr_ehi_ora_ehadmin.CUSTOMER_SCRIPT_SESSION_DCMNT', 'ods_pr_ehi_ora_ehadmin.CUSTOMER_SCRIPT_SESSION_DCMNT',
         'ehadmin.CUSTOMER_SCRIPT_SESSION_DCMNT'),
        ('ods_pr_ehi_ora_ehadmin.PLAN_BENEFITS', 'ods_pr_ehi_ora_ehadmin.PLAN_BENEFITS', 'ehadmin.PLAN_BENEFITS'),
        ('ods_pr_ehi_ora_ehadmin.SG_APPLICATION', 'ods_pr_ehi_ora_ehadmin.SG_APPLICATION', 'ehadmin.SG_APPLICATION'),
        ('ods_pr_ehi_ora_ehadmin.RIDER_CATEGORY', 'ods_pr_ehi_ora_ehadmin.RIDER_CATEGORY', 'ehadmin.RIDER_CATEGORY'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_TYPES', 'ods_pr_ehi_ora_ehadmin.LEAD_TYPES', 'ehadmin.LEAD_TYPES'),
        ('ods_pr_ehi_ora_ehadmin.BUNDLE_APPLICATION', 'ods_pr_ehi_ora_ehadmin.BUNDLE_APPLICATION',
         'ehadmin.BUNDLE_APPLICATION'),
        ('ods_pr_ehi_ora_ehadmin.BO_FOLLOW_UP_TRACKING', 'ods_pr_ehi_ora_ehadmin.BO_FOLLOW_UP_TRACKING',
         'ehadmin.BO_FOLLOW_UP_TRACKING'),
        ('ods_pr_ehi_ora_ehadmin.DOCUMENT_TEMPLATE', 'ods_pr_ehi_ora_ehadmin.DOCUMENT_TEMPLATE',
         'ehadmin.DOCUMENT_TEMPLATE'),
        ('ods_pr_ehi_ora_ehadmin.LEAD_WORK_QUEUE', 'ods_pr_ehi_ora_ehadmin.LEAD_WORK_QUEUE', 'ehadmin.LEAD_WORK_QUEUE'),
        ('ods_pr_ehi_ora_ehadmin.MC_BO_USER_CARRIER_CERTIFY', 'ods_pr_ehi_ora_ehadmin.MC_BO_USER_CARRIER_CERTIFY',
         'ehadmin.MC_BO_USER_CARRIER_CERTIFY'),
        ('ods_pr_ehi_ora_ehadmin.MC_BO_USER_CARRIER_FAMILY', 'ods_pr_ehi_ora_ehadmin.MC_BO_USER_CARRIER_FAMILY',
         'ehadmin.MC_BO_USER_CARRIER_FAMILY'),
        ('ods_pr_ehi_ora_ehadmin.MC_BO_USER_LICENSE_INFO', 'ods_pr_ehi_ora_ehadmin.MC_BO_USER_LICENSE_INFO',
         'ehadmin.MC_BO_USER_LICENSE_INFO'),
        ('ods_pr_ehi_ora_ehadmin.SG_DOCUMENT', 'ods_pr_ehi_ora_ehadmin.SG_DOCUMENT', 'ehadmin.SG_DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.UM_ROLE', 'ods_pr_ehi_ora_ehadmin.UM_ROLE', 'ehadmin.UM_ROLE'),
        ('ods_pr_ehi_ora_ehadmin.UM_USER_ROLE', 'ods_pr_ehi_ora_ehadmin.UM_USER_ROLE', 'ehadmin.UM_USER_ROLE'),
        ('ods_pr_ehi_ora_ehadmin.WORK_QUEUE_DOCUMENT', 'ods_pr_ehi_ora_ehadmin.WORK_QUEUE_DOCUMENT',
         'ehadmin.WORK_QUEUE_DOCUMENT'),
        ('ods_pr_ehi_ora_ehadmin.USER_SALES_REP_HISTORY', 'ods_pr_ehi_ora_ehadmin.USER_SALES_REP_HISTORY',
         'ehadmin.USER_SALES_REP_HISTORY')
    ]
    for tbl_name in tables:
        main(source1, source1_name, source2, source2_name, source3, source3_name, tbl_name[0], tbl_name[1], tbl_name[2])
