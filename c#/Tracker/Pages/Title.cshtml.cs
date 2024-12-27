using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace Tracker.Pages
{
    public class Title : PageModel
    {
        private readonly ILogger<Title> _logger;

        public Title(ILogger<Title> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }
    }
}