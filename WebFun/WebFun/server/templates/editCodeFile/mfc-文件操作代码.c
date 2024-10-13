void IterAllFile(CString strFolder)
{
	CFileFind finder;
	BOOL bWorking = finder.FindFile(strFolder);

	while (bWorking) 
	{ 
		bWorking = finder.FindNextFile();

		if(finder.IsDots())
			continue;
		if (finder.IsDirectory())
		{
			////递归调用
			IterAllFile(finder.GetFilePath() + _T("\\*"));
		}
		else
		{
			CString strFilePath = finder.GetFilePath();
			CString strFileName = finder.GetFileName();

			//获取文件类型
			int nIndex = strFileName.ReverseFind('.');
			CString strFileExt = strFileName.Right(strFileName.GetLength() - nIndex);

			if(strFileExt.CompareNoCase(_T(".txt")) == 0)
			{
				int nIndex = strFileName.Find('-');
				CString strFileId = strFileName.Left(nIndex);

				CStdioFile csFile;
				if(csFile.Open(strFilePath,CFile::modeRead))
				{
					CString strRowData;
					while(csFile.ReadString(strRowData))//每行数据初始化
					{
						if (strRowData.GetAt(0) == 'x')
						{
							continue;
						}
						FILENODE fNode;
						fNode.m_strFilePath = strFilePath;
						fNode.m_strFileName = strFileName;
						fNode.m_strFileId = strFileId;

						//分割
						int nPos = 0;//指针当前位置
						CString strVal;
						CString strKey;
						CString strCol3;
						CString strTmp = strRowData;
						int nColFlag = 0;

						while(1)
						{
							int nIndex = strTmp.Find(_T('	'));
							if (nIndex == -1)
							{
								strVal = strTmp;
								break;
							}
							else
							{
								if (nColFlag == 0)
								{
									strKey = strTmp.Mid(nPos,nIndex);
								}
								else if(nColFlag == 1)
								{
									strCol3 = strTmp.Mid(nPos,nIndex);
								}
									
							}

							strTmp = strTmp.Right(strTmp.GetLength() - nIndex-1);
							++nColFlag;

						}

						if (nColFlag > 0)
						{
							fNode.m_dCol1 = _wtof(strKey);
							fNode.m_dCol2 = _wtof(strCol3);
							fNode.m_dCol3 = _wtof(strVal);
						}

						g_arrFileNode.Add(fNode);
						g_allFileMap[strKey] += (fNode.m_strFilePath + _T('?'));
					}

				}
			}
			
		}
	}
	finder.Close();

	////
	//USES_CONVERSION;
	//CFile file;
	//if(file.Open(_T("test.txt"),CFile::modeCreate|CFile::modeReadWrite))
	//{
	//	for (int i =0;i<g_arrFileNode.GetCount();++i)
	//	{	
	//		CString strFileId = g_arrFileNode[i].m_strFileId;
	//		CString strText;
	//		strText.Format(_T("%s,%f,%f,%f"),strFileId,g_arrFileNode[i].m_dCol1,g_arrFileNode[i].m_dCol2,g_arrFileNode[i].m_dCol3);

	//		char * pFileName = T2A(strText);   
	//		file.Write(pFileName,wcslen(strText));
	//		file.Write("\n",1);
	//	}

	//}
	//file.Close();

}
