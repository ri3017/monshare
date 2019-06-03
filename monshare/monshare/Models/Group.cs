﻿using System;
using System.Collections.Generic;
using System.Json;
using System.Text;

namespace monshare.Models
{
    class Group
    {
        public int GroupId { get; internal set; }
        public string Title { get; internal set; }
        public string Description { get; internal set; }
        public DateTime CreationDateTime { get; internal set; }
        public DateTime EndDateTime { get; internal set; }
        public int MembersNumber { get; internal set; }
        public int TargetNumberOfPeople { get; internal set; }
        public int OwnerId { get; internal set; }
    }
}